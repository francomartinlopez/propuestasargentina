// Se ejecuta sola cada vez que Netlify recibe un envío de formulario válido (no spam).
// 1) Manda el mensaje completo del formulario "contacto" al autor, con "Responder a" dirigido a quien escribió.
// 2) Manda a quien escribió un aviso de recepción fijo, sin repetir su mensaje.
// Variables de entorno (Netlify → Site configuration → Environment variables):
//   GMAIL_USER          cuenta de Gmail que envía
//   GMAIL_APP_PASSWORD  contraseña de aplicación de esa cuenta
//   NOTIFY_TO           a quién llega el mensaje (si falta, se usa GMAIL_USER)
import nodemailer from 'nodemailer';

const limpio = (v) => String(v ?? '').trim();
const esMail = (v) => /^[^\s@<>,;]+@[^\s@<>,;]+\.[^\s@<>,;]+$/.test(v);

const AVISO = [
  'Hola:',
  '',
  'Recibimos tu mensaje en 100 propuestas para la Argentina. Gracias por escribir.',
  'Lo leemos todo; si hace falta una respuesta, te va a llegar a este mismo correo.',
  '',
  'Este es un aviso automático: no hace falta que lo contestes.',
  '',
  'propuestasargentina.netlify.app',
].join('\n');

export const handler = async (event) => {
  try {
    const { payload } = JSON.parse(event.body || '{}');
    if (!payload || payload.form_name !== 'contacto') return { statusCode: 200, body: 'ignorado' };
    const d = payload.data || {};
    const user = process.env.GMAIL_USER, pass = process.env.GMAIL_APP_PASSWORD;
    if (!user || !pass) { console.error('Faltan GMAIL_USER o GMAIL_APP_PASSWORD'); return { statusCode: 200, body: 'sin credenciales' }; }
    const to = process.env.NOTIFY_TO || user;
    const email = limpio(d.email);
    const valido = esMail(email);
    const campos = [
      ['Motivo', d.motivo], ['Nombre', d.nombre], ['Provincia', d.provincia], ['Localidad', d.localidad],
      ['Correo', email], ['Teléfono o WhatsApp', d.telefono || '(no lo dejó)'], ['Mensaje', d.mensaje],
    ];
    const texto = 'Mensaje enviado desde el formulario de 100 propuestas para la Argentina.\n\n' +
      campos.map(([k, v]) => `${k}: ${limpio(v)}`).join('\n') +
      (valido ? '\n\nRespondé a este correo para contestarle a quien escribió.' : '\n\nNo dejó un correo válido.');
    const transporte = nodemailer.createTransport({ service: 'gmail', auth: { user, pass } });
    await transporte.sendMail({
      from: `"100 propuestas" <${user}>`,
      to,
      replyTo: valido ? email : undefined,
      subject: `Contacto: ${limpio(d.motivo)} · ${limpio(d.nombre)} · ${limpio(d.provincia)}`.slice(0, 180),
      text: texto,
    });
    if (valido) {
      try {
        await transporte.sendMail({
          from: `"100 propuestas" <${user}>`,
          to: email,
          subject: 'Recibimos tu mensaje · 100 propuestas para la Argentina',
          text: AVISO,
        });
      } catch (e) { console.error('No se pudo mandar el aviso de recepción:', e); }
    }
    return { statusCode: 200, body: 'enviado' };
  } catch (e) {
    console.error('Error al enviar el correo:', e);
    return { statusCode: 200, body: 'error' };
  }
};
