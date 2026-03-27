using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace InventorySystem
{
    public sealed partial class InventoryForm : Window
    {
        public InventoryForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void dgvProducts_CellClick(object sender, RoutedEventArgs e)
        {
            if (dgvProducts.CurrentRow != null)
                        {
                            txtProductName.Text = dgvProducts.CurrentRow.Cells[0].Value.ToString();
                            cmbCategory.Text = dgvProducts.CurrentRow.Cells[1].Value.ToString();
                            nudPrice.Value = Convert.ToDecimal(dgvProducts.CurrentRow.Cells[2].Value);
                            nudQuantity.Value = Convert.ToInt32(dgvProducts.CurrentRow.Cells[3].Value);
                        }
        }

        // Migrated from WinForms event handler
        private void dgvProducts_CellValueChanged(object sender, RoutedEventArgs e)
        {
            UpdateTotals();
        }

        // Migrated from WinForms event handler
        private void txtProductName_TextChanged(object sender, TextChangedEventArgs e)
        {
            btnAdd.Enabled = txtProductName.Text.Length > 0;
        }

        // Migrated from WinForms event handler
        private void cmbCategory_Changed(object sender, SelectionChangedEventArgs e)
        {
            FilterByCategory(cmbCategory.SelectedItem?.ToString());
        }

        // Migrated from WinForms event handler
        private void nudPrice_ValueChanged(object sender, RoutedEventArgs e)
        {
            UpdateTotals();
        }

        // Migrated from WinForms event handler
        private void btnAdd_Click(object sender, RoutedEventArgs e)
        {
            dgvProducts.Rows.Add(txtProductName.Text, cmbCategory.Text, nudPrice.Value, nudQuantity.Value, DateTime.Now);
                        UpdateTotals();
                        ClearFields();
        }

        // Migrated from WinForms event handler
        private void btnUpdate_Click(object sender, RoutedEventArgs e)
        {
            if (dgvProducts.CurrentRow != null)
                        {
                            dgvProducts.CurrentRow.Cells[0].Value = txtProductName.Text;
                            dgvProducts.CurrentRow.Cells[1].Value = cmbCategory.Text;
                            dgvProducts.CurrentRow.Cells[2].Value = nudPrice.Value;
                            UpdateTotals();
                        }
        }

        // Migrated from WinForms event handler
        private void btnDelete_Click(object sender, RoutedEventArgs e)
        {
            if (dgvProducts.CurrentRow != null && await ShowDialogAsync("Delete?", "Confirm", MessageBoxButtons.YesNo) == ContentDialogResult.Yes)
                        {
                            dgvProducts.Rows.Remove(dgvProducts.CurrentRow);
                            UpdateTotals();
                        }
        }

        // Migrated from WinForms event handler
        private void btnExport_Click(object sender, RoutedEventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog();
                        sfd.Filter = "CSV|*.csv";
                        if (sfd.ShowDialog() == ContentDialogResult.OK)
                        {
                            using (var writer = new System.IO.StreamWriter(sfd.FileName))
                            {
                                foreach (DataGridViewRow row in dgvProducts.Rows)
                                    writer.WriteLine(string.Join(",", row.Cells.Cast<DataGridViewCell>().Select(c => c.Value)));
                            }
                        }
        }

        // Migrated from WinForms event handler
        private void txtSearch_TextChanged(object sender, TextChangedEventArgs e)
        {
            foreach (DataGridViewRow row in dgvProducts.Rows)
                        {
                            row.Visible = row.Cells[0].Value?.ToString().Contains(txtSearch.Text, StringComparison.OrdinalIgnoreCase) ?? false;
                        }
        }

        // Migrated from WinForms event handler
        private void chkLowStock_Changed(object sender, RoutedEventArgs e)
        {
            foreach (DataGridViewRow row in dgvProducts.Rows)
                        {
                            if (chkLowStock.Checked)
                                row.Visible = Convert.ToInt32(row.Cells[3].Value) < 10;
                            else
                                row.Visibility = Visibility.Visible;
                        }
        }

        // Migrated from WinForms event handler
        private void autoRefreshTimer_Tick(object sender, object e)
        {
            UpdateTotals();
                        lblTotal.Text = $"Total: {dgvProducts.Rows.Count} items";
        }
    }
}