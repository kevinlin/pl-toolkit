import csv
from csv_converter import csv_to_articles


def test_csv_to_articles(tmp_path):
    input_csv = tmp_path / "input.csv"
    output_dir = tmp_path / "out"
    long_text = (
        "This is a very long piece of text that exceeds eighty characters in total. "
        "It contains multiple sentences. Ensure newline."
    )

    with open(input_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "description", "name"])
        writer.writerow(["1", long_text, "Test Name"])

    csv_to_articles(str(input_csv), str(output_dir))

    output_file = output_dir / "Test_Name.txt"
    assert output_file.exists()

    content = output_file.read_text()
    expected = "description:\n" + long_text.replace(". ", ".\n") + "\n\n"
    assert expected in content
