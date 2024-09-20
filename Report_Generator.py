import os
import csv


def generate_html_report(csv_file="log.csv", html_file="report.html"):
    if not os.path.exists(csv_file):
        print(f"{csv_file} does not exist.")
        return

    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Create an HTML file with CSS styling
    with open(html_file, "w") as file:
        file.write("<html><head><title>DMARC and SPF Log Report</title>")
        file.write("<style>")
        file.write("body { font-family: Arial, sans-serif; margin: 20px; }")
        file.write("h1 { color: #333; }")
        file.write(
            "table { width: 100%; border-collapse: collapse; margin-top: 20px; }"
        )
        file.write(
            "th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }"
        )
        file.write("th { background-color: #f2f2f2; }")
        file.write("tr:nth-child(even) { background-color: #f9f9f9; }")
        file.write("tr:hover { background-color: #f1f1f1; }")
        file.write("</style>")
        file.write("<script>")
        file.write("""
        function filterTable() {
            const table = document.getElementById('logTable');
            const rows = table.getElementsByTagName('tr');
            const filterInputs = document.querySelectorAll('input[type="text"]');

            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                let showRow = true;

                for (let j = 0; j < cells.length; j++) {
                    const filterValue = filterInputs[j].value.toLowerCase();
                    const cellText = cells[j].innerText.toLowerCase();
                    
                    // Check if the cell starts with the filter value
                    if (filterValue && !cellText.startsWith(filterValue)) {
                        showRow = false;
                        break;
                    }
                }
                rows[i].style.display = showRow ? '' : 'none';
            }
        }
        """)
        file.write("</script>")
        file.write("</head><body>")
        file.write("<h1>DMARC and SPF Log Report</h1>")
        file.write("<table id='logTable'>")

        file.write("<tr>")
        for header in rows[0]:
            file.write(
                f"<th>{header} <input type='text' onkeyup='filterTable()' placeholder='Filter A-Z...'></th>"
            )
        file.write("</tr>")

        for row in rows[1:]:
            file.write("<tr>")
            for column in row:
                file.write(f"<td>{column}</td>")
            file.write("</tr>")

        file.write("</table>")
        file.write("</body></html>")

    print(f"HTML report generated: {html_file}")


if __name__ == "__main__":
    generate_html_report()
