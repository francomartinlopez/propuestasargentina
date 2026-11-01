// Se ejecuta sola cada vez que Netlify recibe un envío de formulario válido (no spam).
// Manda el mensaje del formulario "contacto" al autor, con copia a quien lo escribió.
// Variables de entorno (Netlify → Site configuration → Environment variables):
//   GMAIL_USER          cuenta de Gmail que envía
//   GMAIL_APP_PASSWORD  contraseña de aplicación de esa cuenta
//   NOTIFY_TO           a quién llega (si falta, se usa GMAIL_USER)
import nodemailer from 'nodemailer';

const limpio = (v) => String(v ?? '').trim();
const esMail = (v) => /^[^\s@<>,;]+@[^\s@<>,;]+\.[^\s@<>,;]+$/.test(v);

export const handler = async (event) => {
  try {
    const { payload } = JSON.parse(event.body || '{}');
    if (!payload || payload.form_name !== 'contacto') return { statusCode: 200, body: 'ignorado' };
    const d = payload.data || {};
    const user = process.env.GMAIL_USER, pass = process.env.GMAIL_APP_PASSWORD;
    if (!user || !pass) { console.error('Faltan GMAIL_USER o GMAIL_APP_PASSWORD'); return { statusCode: 200, body: 'sin credenciales' }; }
    const to = process.env.NOTIFY_TO || user;
    const email = limpio(d.email);
    const campos = [
      ['Motivo', d.motivo], ['Nombre', d.nombre], ['Provincia', d.provincia],
      ['Correo', email], ['Teléfono o WhatsApp', d.telefono || '(no lo dejó)'], ['Mensaje', d.mensaje],
    ];
    const texto = 'Esta es una copia del mensaje enviado desde el formulario de 100 propuestas para la Argentina.\n\n' +
      campos.map(([k, v]) => `${k}: ${limpio(v)}`).join('\n') +
      '\n\nRespondé a este correo para contestarle a quien escribió.';
    const transporte = nodemailer.createTransport({ service: 'gmail', auth: { user, pass } });
    await transporte.sendMail({
      from: `"100 propuestas" <${user}>`,
      to,
      cc: esMail(email) ? email : undefined,
      replyTo: esMail(email) ? email : undefined,
      subject: `Contacto: ${limpio(d.motivo)} · ${limpio(d.nombre)} · ${limpio(d.provincia)}`.slice(0, 180),
      text: texto,
    });
    return { statusCode: 200, body: 'enviado' };
  } catch (e) {
    console.error('Error al enviar el correo:', e);
    return { statusCode: 200, body: 'error' };
  }
};
