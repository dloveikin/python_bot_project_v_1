from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate

c = SimpleDocTemplate("hello.pdf", pagesize=(1063, 591))
# c.drawString(100,400,"Welcome to Reportlab!")

# c.setLineWidth(.3)
# c.setFont('Helvetica', 12)

#
# c.drawString(30,750,'OFFICIAL COMMUNIQUE')
# c.line(100,400,400,400)

Story = []
logo = "dunulo.jpg"
im = Image(logo, 100, 100)
Story.append(im)
c.build(Story)

# c.save()