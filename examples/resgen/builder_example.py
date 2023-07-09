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
            },
            {
                "component": "resgen.components.experience.Experience",
                "title": "TITLE",
                "experience_start": "2020 Jan",
                "experience_end": "2023 June",
                "description": "NOTHING",
            },
        ]

    )
    builder.build()


if __name__ == "__main__":
    main()
