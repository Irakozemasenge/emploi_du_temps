from collections import deque
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
)


class Queue(deque):
    def pop(self):
        return self.popleft()


Profs = {
    "1": {"id": 1, "nom": "Dr. MUKESHIMANA Michèle"},
    "2": {"id": 2, "nom": "Msc RWIMO Samuel"},
    "3": {"id": 3, "nom": "Dr. SAHINGUVU William"},
    "4": {"id": 4, "nom": "Dr. NDAYISABA Longin"},
    "5": {"id": 5, "nom": "Msc CIZA Innocent"},
    "6": {"id": 6, "nom": "Msc NDAYITEZIBIGANZA Thierry"},
    "7": {"id": 7, "nom": "Msc IRIHO Kévin"},
    "none": {"nom": ""},
}

ECUs = {
    "1": {
        "id": 1,
        "ue": 1,
        "nom": "Intelligence artificielle",
        "Credits": 4,
        "prof": "1",
    },
    "2": {
        "id": 2,
        "ue": 1,
        "nom": "Machine Learning",
        "Credits": 4,
        "prof": "1",
    },
    "3": {
        "id": 3,
        "ue": 2,
        "nom": "Maintenance des systèmes",
        "Credits": 4,
        "prof": "2",
    },
    "4": {
        "id": 4,
        "ue": 2,
        "nom": "Audit informatique",
        "Credits": 3,
        "prof": "3",
    },
    "5": {
        "id": 5,
        "ue": 2,
        "nom": "Fiabilité des systèmes",
        "Credits": 3,
        "prof": "4",
    },
    "6": {
        "id": 6,
        "ue": 3,
        "nom": "Applications Web",
        "Credits": 3,
        "prof": "5",
    },
    "7": {"id": 7, "ue": 3, "nom": "E-commerce", "Credits": 3, "prof": "3"},
    "8": {"id": 8, "ue": 4, "nom": "Robotique", "Credits": 3, "prof": "6"},
    "9": {
        "id": 9,
        "ue": 4,
        "nom": "Test et simulation de systèmes",
        "Credits": 3,
        "prof": "7",
    },
}


def create_pdf(filename, rows):
    """Crée un PDF avec l'horaire."""
    pdf = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Titre du document
    title = Paragraph("Horaire", styles["Title"])
    n = Paragraph(f"Nombre de semaines : {len(rows)}")
    story.append(title)
    story.append(n)
    story.append(Spacer(1, 12))

    # Créer une table pour chaque semaine
    for k, week in enumerate(rows):
        data = [["Jours", "1ère séance", "2ème séance", "3ème séance"]]
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        d = 0

        while week:
            sc1 = week.popleft()
            sc2 = week.popleft()
            sc3 = week.popleft()

            row = [
                days[d],
                f"{sc1['nom']}\n{Profs[sc1['prof']]['nom']}",
                f"{sc2['nom']}\n{Profs[sc2['prof']]['nom']}",
                f"{sc3['nom']}\n{Profs[sc3['prof']]['nom']}",
            ]
            data.append(row)
            d += 1

        # Créer la table avec une largeur uniforme
        table = Table(data, colWidths=[50, 160, 160, 160])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        story.append(table)
        if (k + 1) % 3 == 0:
            story.append(PageBreak())
        else:
            story.append(Spacer(1, 12))

    # Générer le PDF
    pdf.build(story)
    print(f"PDF généré avec succès : {filename}")


def main():
    seances = Queue()

    for ecu in ECUs.values():
        for seance in range(ecu["Credits"] * 5):
            seances.append(ecu)

    tpe = {"nom": "TPE", "prof": "none"}

    rows = []

    p = None
    while seances:
        hb_seance = deque()
        for i in range(5):
            if seances:
                p = seances.pop()
                hb_seance.append(p)
            else:
                hb_seance.append(tpe)
            if seances:
                p = seances.pop()
                hb_seance.append(p)
            else:
                hb_seance.append(tpe)
            hb_seance.append(tpe)
            if seances:
                l = seances.pop()
                if l != p:
                    hb_seance.pop()
                    hb_seance.pop()
                    hb_seance.append(tpe)
                    hb_seance.append(l)
        rows.append(hb_seance)

    print(f"Nombre de semaines : {len(rows)}")
    create_pdf("Emploi_du_temps.pdf", rows)


if __name__ == "__main__":
    main()
