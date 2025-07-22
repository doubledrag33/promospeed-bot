const express = require("express");
const axios   = require("axios");
const bodyParser = require("body-parser");

const app  = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

// 1) Endpoint di verifica webhook (GET)
app.get("/webhook", (req, res) => {
  const mode      = req.query["hub.mode"];
  const token     = req.query["hub.verify_token"];
  const challenge = req.query["hub.challenge"];
  if (mode === "subscribe" && token === process.env.VERIFY_TOKEN) {
    console.log("WEBHOOK_VERIFIED");
    return res.status(200).send(challenge);
  }
  return res.sendStatus(403);
});

// 2) Gestione messaggi in arrivo (POST)
app.post("/webhook", async (req, res) => {
  const entries = req.body.entry || [];
  for (const entry of entries) {
    for (const change of entry.changes || []) {
      const phoneId = change.value.metadata.phone_number_id;
      for (const message of change.value.messages || []) {
        const text = message.text?.body?.trim().toLowerCase();
        if (text === "promo speedwash") {
          try {
            await axios.post(
              `https://graph.facebook.com/v18.0/${phoneId}/messages`,
              {
                messaging_product: "whatsapp",
                to: message.from,
                type: "text",
                text: {
                  body: `Ecco come funziona la Promo Speedwash:\n1) Lavaggio interno rapido\n2) Dettagli esterni\n3) Asciugatura rapida\nContattaci per conferma!`
                }
              },
              { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
            );
          } catch (err) {
            console.error("Errore invio risposta:", err.response?.data || err.message);
          }
        }
      }
    }
  }
  res.sendStatus(200);
});

app.listen(port, () => console.log(`Promo Speedwash bot live on port ${port}`));
