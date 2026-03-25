from flask import Flask, request, Response
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

@app.route("/pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.get_json()
        html_content = data.get("html", "")
        
        if not html_content:
            return {"error": "HTML content is required"}, 400
        
        options = data.get("options", {})
        
        font_config = FontConfiguration()
        html = HTML(string=html_content)
        
        pdf_bytes = html.write_pdf(font_config=font_config)
        
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=documento.pdf",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
            }
        )
    except Exception as e:
        logging.error(f"PDF generation error: {e}")
        return {"error": str(e)}, 500

@app.route("/pdf", methods=["OPTIONS"])
def pdf_options():
    return Response(
        "ok",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
        }
    )

if __name__ == "__main__":
    port = int(__import__("os").environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
