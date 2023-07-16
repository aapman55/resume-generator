from resgen.core.builder import DocumentBuilder


def main() -> None:
    builder = DocumentBuilder(
        page_settings={
            "sidebar": {
                "fill_colour": {
                    "r": 255,
                    "g": 50,
                    "b": 50,
                }
            }
        },
        output_name="builder_example.pdf",
        style_registry={
            "styles": [
                {
                    "id": "general",
                    "family": "Helvetica",
                },
                {
                    "id": "tektur",
                    "family": "Tektur",
                },
            ]
        },
        custom_fonts=[
            {
                "family": "Tektur",
                "font_file_path": "./custom_fonts/Tektur-Regular.ttf",
            },
        ],
        components=[
            {
                "component": "resgen.components.experience.Experience",
                "title": "TITLE",
                "experience_start": "2020 Jan",
                "experience_end": "2023 June",
                "description": "NOTHING",
                "general_style": "general",
                "top_padding": 10,
                # "left_padding": 100,
                "fill_colour": {
                    "r": 200,
                    "g": 200,
                    "b": 200,
                },
            },
            {
                "component": "resgen.components.experience.Experience",
                "title": "TITLE",
                "experience_start": "2020 Jan",
                "experience_end": "2023 June",
                "description": "NOTHINGllllll lllllllllllllll llllllllllllll lllllllllllllll llllllllllll",
                "general_style": "tektur",
                # "right_padding": 100,
            },
        ],
    )
    builder.build()


if __name__ == "__main__":
    main()
