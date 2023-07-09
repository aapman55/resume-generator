from resgen.core.builder import DocumentBuilder


def main() -> None:
    builder = DocumentBuilder(
        output_name="builder_example.pdf",
        components=[
            {
                "component": "resgen.components.experience.Experience",
                "title": "TITLE",
                "experience_start": "2020 Jan",
                "experience_end": "2023 June",
                "description": "NOTHING",
                "top_padding": 30,
                "left_padding": 100,
                "fill_colour": {
                    "r": 200,
                    "g": 200,
                    "b": 200,
                }
            },
            {
                "component": "resgen.components.experience.Experience",
                "title": "TITLE",
                "experience_start": "2020 Jan",
                "experience_end": "2023 June",
                "description": "NOTHINGllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll",
                "right_padding": 100,
            },
        ]

    )
    builder.build()


if __name__ == "__main__":
    main()
