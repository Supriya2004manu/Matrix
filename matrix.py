import flet as ft
import csv
import numpy as np
import random


def main(page: ft.Page):
    page.title = "Matrix Operations App"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Header and styling for the app title
    title = ft.Text(
        "Matrix Operations App",
        size=36,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.LIGHT_BLUE_400
    )
    subtitle = ft.Text(
        "Perform operations such as addition, subtraction, and multiplication on matrices.",
        size=16,
        color=ft.colors.GREY_500
    )

    # Matrix size inputs with clear labels and styling
    n_input = ft.TextField(
        label="Matrix A Rows (n):",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_matrix_inputs(),
        width=150,
        border_radius=12,
        filled=True,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.DEEP_PURPLE_900
    )

    m_input = ft.TextField(
        label="Matrix B Columns (m):",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_matrix_inputs(),
        width=150,
        border_radius=12,
        filled=True,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.DEEP_PURPLE_900
    )

    # UI elements for matrices and result display
    matrix_a = []
    matrix_b = []
    result_display = ft.Column(spacing=12)
    matrix_a_column = ft.Column(spacing=12)
    matrix_b_column = ft.Column(spacing=12)

    # Functions for generating and displaying matrix input fields
    def create_matrix_inputs(n, m):
        nonlocal matrix_a, matrix_b
        matrix_a, matrix_b = [], []
        matrix_a_column.controls.clear()
        matrix_b_column.controls.clear()

        for i in range(n):
            row_a = []
            for j in range(m):
                row_a.append(
                    ft.TextField(width=50, text_align=ft.TextAlign.CENTER, filled=True, bgcolor=ft.colors.GREY_900,
                                 border_radius=8))
            matrix_a.append(row_a)
            matrix_a_column.controls.append(ft.Row(row_a, alignment=ft.MainAxisAlignment.CENTER))

        for i in range(m):
            row_b = []
            for j in range(n):
                row_b.append(
                    ft.TextField(width=50, text_align=ft.TextAlign.CENTER, filled=True, bgcolor=ft.colors.GREY_900,
                                 border_radius=8))
            matrix_b.append(row_b)
            matrix_b_column.controls.append(ft.Row(row_b, alignment=ft.MainAxisAlignment.CENTER))

        page.update()

    # Helper functions
    def generate_random_matrices(e):
        try:
            n, m = int(n_input.value), int(m_input.value)
            for i in range(n):
                for j in range(m):
                    matrix_a[i][j].value = str(round(random.uniform(-10, 10), 2))
            for i in range(m):
                for j in range(n):
                    matrix_b[i][j].value = str(round(random.uniform(-10, 10), 2))
            page.update()
        except ValueError:
            display_error("Please enter positive integers for matrix dimensions.")

    def import_from_csv(e):
        page.dialog(ft.FilePickerDialog(), on_select=handle_file_select)

    def handle_file_select(e):
        if e.files:
            filename = e.files[0].path
            try:
                with open(filename, newline='') as file:
                    reader = csv.reader(file)
                    matrix_a.clear()
                    for i in range(len(matrix_a)):
                        row = next(reader)
                        matrix_a.append([ft.TextField(value=row[j], width=50, text_align=ft.TextAlign.CENTER,
                                                      filled=True, bgcolor=ft.colors.GREY_900, border_radius=8) for j in
                                         range(len(row))])
                    matrix_a_column.controls.clear()
                    for row in matrix_a:
                        matrix_a_column.controls.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER))

                    matrix_b.clear()
                    for i in range(len(matrix_b)):
                        row = next(reader)
                        matrix_b.append([ft.TextField(value=row[j], width=50, text_align=ft.TextAlign.CENTER,
                                                      filled=True, bgcolor=ft.colors.GREY_900, border_radius=8) for j in
                                         range(len(row))])
                    matrix_b_column.controls.clear()
                    for row in matrix_b:
                        matrix_b_column.controls.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER))

                    page.update()

            except Exception as e:
                display_error(f"Failed to import: {str(e)}")

    def calculate_matrices(operation):
        try:
            n, m = int(n_input.value), int(m_input.value)
            matrix_a_values = np.array([[float(matrix_a[i][j].value or 0) for j in range(m)] for i in range(n)])
            matrix_b_values = np.array([[float(matrix_b[i][j].value or 0) for j in range(n)] for i in range(m)])

            if operation == "add":
                result_matrix = matrix_a_values + matrix_b_values
            elif operation == "subtract":
                result_matrix = matrix_a_values - matrix_b_values
            elif operation == "multiply":
                result_matrix = np.dot(matrix_a_values, matrix_b_values)

            display_result(result_matrix, operation)

        except ValueError as e:
            display_error(str(e))
        except Exception as e:
            display_error(f"An error occurred: {str(e)}")

    def display_result(result_matrix, operation):
        result_display.controls.clear()
        result_display.controls.append(ft.Text(f"{operation.capitalize()} Result:", size=20, color=ft.colors.CYAN))
        if isinstance(result_matrix, np.ndarray):
            for row in result_matrix:
                result_display.controls.append(
                    ft.Row(
                        [ft.Text(f"{value:.2f}", width=50, text_align=ft.TextAlign.CENTER, color=ft.colors.YELLOW) for
                         value in row],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
        page.update()

    def display_error(message):
        result_display.controls.clear()
        result_display.controls.append(ft.Text(message, color=ft.colors.RED))
        page.update()

    def update_matrix_inputs():
        try:
            n, m = int(n_input.value), int(m_input.value)
            create_matrix_inputs(n, m)
        except ValueError:
            display_error("Invalid matrix dimensions. Please enter valid integers.")

    def export_to_csv(e):
        try:
            with open("matrix_results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Matrix A"])
                for row in matrix_a:
                    writer.writerow([cell.value or 0 for cell in row])
                writer.writerow([])
                writer.writerow(["Matrix B"])
                for row in matrix_b:
                    writer.writerow([cell.value or 0 for cell in row])
                writer.writerow([])
                writer.writerow(["Result"])
                if len(result_display.controls) > 1:
                    for control in result_display.controls[1:]:
                        writer.writerow([text.value for text in control.controls])

            display_error("Results exported to matrix_results.csv")
        except Exception as e:
            display_error(f"Failed to export: {str(e)}")

    # Buttons with updated colors and layout
    button_color = ft.colors.CYAN
    page.add(
        ft.Column([
            title,
            subtitle,
            ft.Row([n_input, m_input]),
            ft.Row([
                ft.ElevatedButton("Add", color=button_color, on_click=lambda e: calculate_matrices("add")),
                ft.ElevatedButton("Subtract", color=button_color, on_click=lambda e: calculate_matrices("subtract")),
                ft.ElevatedButton("Multiply", color=button_color, on_click=lambda e: calculate_matrices("multiply")),
                ft.ElevatedButton("Random Matrices", color=ft.colors.GREEN, on_click=generate_random_matrices),
                ft.ElevatedButton("Import CSV", color=ft.colors.GREEN, on_click=import_from_csv),
                ft.ElevatedButton("Export CSV", color=ft.colors.GREEN, on_click=export_to_csv),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Divider(color=ft.colors.GREY_800, thickness=1),
            ft.Text("Matrix A", size=20, color=ft.colors.CYAN, weight=ft.FontWeight.BOLD),
            matrix_a_column,
            ft.Text("Matrix B", size=20, color=ft.colors.CYAN, weight=ft.FontWeight.BOLD),
            matrix_b_column,
            result_display
        ])
    )

    create_matrix_inputs(2, 2)  # Start with a 2x2 matrix


# Run the app
ft.app(target=main)
