from resgen.core.builder import DocumentBuilder


def main() -> None:
    builder = DocumentBuilder(
        page_settings={
          "sidebar": {
            "fill_colour": {
                "r": 50,
                "g": 50,
                "b": 50,
            }
          }
        },
        output_name="builder_example.pdf",
        components=[
            {
                "component": "resgen.components.experience.Experience",
                "title": "TITLE",
                "experience_start": "2020 Jan",
                "experience_end": "2023 June",
                "description": "NOTHING",
                "top_padding": 30,
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
                # "right_padding": 100,
            },
        ],
    )
    builder.build()


if __name__ == "__main__":
    main()
