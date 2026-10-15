document.querySelectorAll("[data-export-pdf]").forEach(button => {
  button.addEventListener("click", async () => {
    const errorBox = document.getElementById("error");
    button.disabled = true;

    try {
      const {jsPDF} = window.jspdf || {};
      if (!jsPDF) {
        throw new Error("PDF export could not load. Check your internet connection and try again.");
      }

      const pdf = new jsPDF();
      const margin = 16;
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      let y = 18;

      const addText = (text, options = {}) => {
        const {size = 11, bold = false, gap = 6} = options;
        pdf.setFont("helvetica", bold ? "bold" : "normal");
        pdf.setFontSize(size);
        const lines = pdf.splitTextToSize(String(text), pageWidth - margin * 2);
        const height = lines.length * size * 0.45;
        if (y + height > pageHeight - margin) {
          pdf.addPage();
          y = margin;
        }
        pdf.text(lines, margin, y);
        y += height + gap;
      };

      addText(document.querySelector(".page-title h1").textContent, {size: 20, bold: true, gap: 4});
      addText(document.querySelector(".formula-banner").innerText.replace(/\s+/g, " "), {size: 10, gap: 8});
      addText(`Parameters: ${document.getElementById("selected").textContent}`, {bold: true, gap: 8});
      addText("Statistical measures", {size: 14, bold: true, gap: 4});
      document.querySelectorAll(".stat-card").forEach(card => {
        addText(`${card.querySelector("span").textContent}: ${card.querySelector("strong").textContent}`);
      });
      addText("Probability results", {size: 14, bold: true, gap: 4});
      addText(`${document.querySelector(".probability-panel .muted").textContent.trim()}: ${document.getElementById("pmf").textContent}`);
      addText(`${document.getElementById("pmf-expression").textContent}`);
      document.querySelectorAll(".cdf-row").forEach(row => {
        addText(`${row.querySelector("span").textContent}: ${row.querySelector("strong").textContent}`);
      });

      const canvas = document.getElementById("pmfChart");
      if (canvas && canvas.width > 0 && canvas.height > 0) {
        const image = canvas.toDataURL("image/jpeg", 0.85);
        const imageWidth = pageWidth - margin * 2;
        const imageHeight = Math.min(imageWidth * canvas.height / canvas.width, 90);
        if (y + imageHeight > pageHeight - margin) {
          pdf.addPage();
          y = margin;
        }
        pdf.addImage(image, "JPEG", margin, y, imageWidth, imageHeight);
      }

      const pdfUrl = URL.createObjectURL(pdf.output("blob"));
      const downloadLink = document.createElement("a");
      downloadLink.href = pdfUrl;
      downloadLink.download = `${button.dataset.exportPdf}.pdf`;
      downloadLink.click();
      window.setTimeout(() => URL.revokeObjectURL(pdfUrl), 1000);
      if (errorBox) errorBox.hidden = true;
    } catch (error) {
      if (!errorBox) throw error;
      errorBox.textContent = error.message || "PDF export failed.";
      errorBox.hidden = false;
    } finally {
      button.disabled = false;
    }
  });
});
