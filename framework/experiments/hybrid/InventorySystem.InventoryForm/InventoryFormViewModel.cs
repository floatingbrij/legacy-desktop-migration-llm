using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace InventorySystem
{
    public partial class InventoryFormViewModel : ObservableObject
    {
        [ObservableProperty]
        private string _txtProductNameValue;

        [ObservableProperty]
        private string _cmbCategoryValue;

        [ObservableProperty]
        private string _nudPriceValue;

        [ObservableProperty]
        private int _txtSearchValue;

        [ObservableProperty]
        private bool _chkLowStockValue;

        [RelayCommand]
        private void btnAdd()
        {
            dgvProducts.Rows.Add(txtProductNameText, cmbCategoryText, nudPriceValue, nudQuantityValue, DateTime.Now);
            UpdateTotals();
            ClearFields();
        }

        [RelayCommand]
        private void btnUpdate()
        {
            if (dgvProducts.CurrentRow != null)
            {
            dgvProducts.CurrentRow.Cells[0].Value = txtProductNameText;
            dgvProducts.CurrentRow.Cells[1].Value = cmbCategoryText;
            dgvProducts.CurrentRow.Cells[2].Value = nudPriceValue;
            UpdateTotals();
            }
        }

        [RelayCommand]
        private async Task btnDeleteAsync()
        {
            if (dgvProducts.CurrentRow != null && await ShowDialogAsync("Delete?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
            dgvProducts.Rows.Remove(dgvProducts.CurrentRow);
            UpdateTotals();
            }
        }

        [RelayCommand]
        private async Task btnExportAsync()
        {
            SaveFileDialog sfd = new SaveFileDialog();
            sfd.Filter = "CSV|*.csv";
            if (sfd.ShowDialog() == DialogResult.OK)
            {
            using (var writer = new System.IO.StreamWriter(sfd.FileName))
            {
            foreach (DataGridViewRow row in dgvProducts.Rows)
            writer.WriteLine(string.Join(",", row.Cells.Cast<DataGridViewCell>().Select(c => cValue)));
            }
            }
        }

    }
}