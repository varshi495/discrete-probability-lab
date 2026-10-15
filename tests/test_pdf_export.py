import unittest

from app import app


class PdfExportTests(unittest.TestCase):
    def test_export_button_and_script_are_available_on_each_distribution(self):
        client = app.test_client()
        for path, filename in (
            ("/binomial", "binomial"),
            ("/poisson", "poisson"),
            ("/geometric", "geometric"),
        ):
            with self.subTest(path=path, filename=filename):
                response = client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(f'data-export-pdf="{filename}"'.encode(), response.data)
                self.assertIn(b"js/pdf-export.js", response.data)
                response.close()

        script = client.get("/static/js/pdf-export.js")
        self.assertEqual(script.status_code, 200)
        self.assertIn(b"downloadLink.download = `${button.dataset.exportPdf}.pdf`", script.data)
        self.assertIn(b"pdf.addImage(image, \"JPEG\"", script.data)
        script.close()

        geometric_page = client.get("/geometric")
        self.assertIn(b"jspdf@2.5.2/dist/jspdf.umd.min.js", geometric_page.data)
        geometric_page.close()


if __name__ == "__main__":
    unittest.main()
