from resgen.core.document import Resume
from resgen.core.font import Font, FontStyle


def main() -> None:
    doc = Resume()
    font_roboto_regular = Font(
        family="Roboto",
        style=FontStyle(""),
        font_file_path = "./custom_fonts/Roboto-Regular.ttf"
    )

    doc.register_font(font_roboto_regular)
    doc.add_page()
    doc.set_font("Roboto")
    doc.text(40, 10, "Hello wrld!")
    doc.set_font("Courier")
    doc.text(80, 10, "Hello wrld!")
    doc.output("font_example.pdf")


if __name__ == "__main__":
    main()