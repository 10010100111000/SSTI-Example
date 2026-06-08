from flask import Flask, render_template, request, render_template_string


app = Flask(__name__)


LAB_METADATA = {
    "title": "Injection Showcase",
    "tagline": "Understand how insecure template rendering can be dangerous.",
    "tips": [
        "Jinja2 templates can access Python objects when not sandboxed.",
        "Look for builtins like config, request, cycler, joiner, lipsum.",
        "Try payloads such as {{7*7}} or {{config.items()}} to explore.",
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

