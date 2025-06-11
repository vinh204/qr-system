from flask import Flask, render_template, request
import qrcode
import io
import base64
from vietqr import VietQR

app = Flask(__name__)

def generate_qr_base64(data):
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@app.route("/")
def home():
    return render_template("text.html")

@app.route("/text", methods=["GET", "POST"])
def text_qr():
    qr_base64 = None
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            qr_base64 = generate_qr_base64(text)
    return render_template("text.html", qr_base64=qr_base64)

@app.route("/vcard", methods=["GET", "POST"])
def vcard_qr():
    qr_base64 = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        parts = name.split(" ", 1)
        last, first = (parts + [""])[:2] 

        adr = address.replace("\n", " ")
        vcard = "\n".join([
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{last};{first};;;",
            f"FN:{name}",
            f"TEL;TYPE=CELL:{phone}",
            f"EMAIL:{email}",
            f"ADR:;;{adr};;;;",
            "END:VCARD"
        ])

        qr_base64 = generate_qr_base64(vcard)

    return render_template("vcard.html", qr_base64=qr_base64)

@app.route("/transfer", methods=["GET", "POST"])
def transfer_qr():
    qr_base64 = None
    if request.method == "POST":
        bank_bin = request.form.get("bank_bin")
        account_number = request.form.get("account_number")
        amount = request.form.get("amount")
        message = request.form.get("message")

        qr = VietQR()
        qr.set_beneficiary_organization(bank_bin, account_number) \
           .set_transaction_amount(amount) \
           .set_additional_data_field_template(message)
        qr_string = qr.build()
        qr_base64 = generate_qr_base64(qr_string)

    return render_template("transfer.html", qr_base64=qr_base64)

if __name__ == "__main__":
    app.run()
