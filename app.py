from flask import Flask, render_template, request, render_template_string


app = Flask(__name__)


LAB_METADATA = {
    "title": "SSTI Injection Showcase",
    "tagline": "了解不安全的 template rendering 如何带来真实风险。",
    "tips": [
        "Jinja2 templates 在未 sandboxed 时可能访问 Python objects。",
        "关注 config、request、cycler、joiner、lipsum 等 builtins 或上下文对象。",
        "可以尝试 {{7*7}} 或 {{config.items()}} 等 payloads 进行探索。",
    ],
    "fake_flag": "THM{this_is_not_the_real_flag}",
}


def insecure_render(payload: str) -> str:
    """
    Intentionally insecure helper to show how SSTI happens.
    DO NOT copy this pattern into production code.
    """

    if not payload:
        return ""

    # render_template_string directly feeds the user input into Jinja2.
    # This is the core SSTI vulnerability we want to demonstrate.
    return render_template_string(
        payload,
        lab=LAB_METADATA,
        config=app.config,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    payload = request.form.get("payload", "")
    rendered_output = ""
    error_message = ""

    if request.method == "POST":
        try:
            rendered_output = insecure_render(payload)
        except Exception as exc:
            error_message = f"{type(exc).__name__}: {exc}"

    return render_template(
        "index.html",
        payload=payload,
        rendered_output=rendered_output,
        error_message=error_message,
        lab=LAB_METADATA,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

