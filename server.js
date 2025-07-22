const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();
const port = process.env.PORT || 3000;
app.use(bodyParser.json());

app.get('/webhook', (req, res) => {
  // Verification handshake with Meta
  const verify_token = process.env.VERIFY_TOKEN;
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];
  if (mode && token && mode === 'subscribe' && token === verify_token) {
    console.log('WEBHOOK_VERIFIED');
    res.status(200).send(challenge);
  } else {
    res.sendStatus(403);
  }
});

app.post('/webhook', async (req, res) => {
  const data = req.body;
  if (data.entry) {
    data.entry.forEach(entry => {
      (entry.changes || []).forEach(change => {
        const messages = change.value.messages;
        if (messages) {
          messages.forEach(async message => {
            const text = message.text && message.text.body;
            if (text && text.trim().toLowerCase() === 'promo speedwash') {
              await axios.post(
                `https://graph.facebook.com/v15.0/${change.value.metadata.phone_number_id}/messages`,
                {
                  messaging_product: 'whatsapp',
                  to: message.from,
                  type: 'text',
                  text: { body: `Ecco come funziona la Promo Speedwash:\n1) Lavaggio interno rapido\n2) Dettagli esterni\n3) Asciugatura rapida\nContattaci per conferma!` }
                },
                { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
              );
            }
          });
        }
      });
    });
  }
  res.sendStatus(200);
});

app.listen(port, () => console.log(`Server running on port ${port}`));
