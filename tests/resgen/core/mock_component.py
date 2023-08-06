from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class EmptyComponent(Component):
    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        pass
