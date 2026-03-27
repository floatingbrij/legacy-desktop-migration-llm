using System;
using System.Windows.Forms;
using System.Drawing;

namespace InventorySystem
{
    public partial class InventoryForm : Form
    {
        public InventoryForm()
        {
            InitializeComponent();
        }

        private void dgvProducts_CellClick(object sender, EventArgs e)
        {
            if (dgvProducts.CurrentRow != null)
            {
                txtProductName.Text = dgvProducts.CurrentRow.Cells[0].Value.ToString();
                cmbCategory.Text = dgvProducts.CurrentRow.Cells[1].Value.ToString();
                nudPrice.Value = Convert.ToDecimal(dgvProducts.CurrentRow.Cells[2].Value);
                nudQuantity.Value = Convert.ToInt32(dgvProducts.CurrentRow.Cells[3].Value);
            }
        }

        private void dgvProducts_CellValueChanged(object sender, EventArgs e)
        {
            UpdateTotals();
        }

        private void txtProductName_TextChanged(object sender, EventArgs e)
        {
            btnAdd.Enabled = txtProductName.Text.Length > 0;
        }

        private void cmbCategory_Changed(object sender, EventArgs e)
        {
            FilterByCategory(cmbCategory.SelectedItem?.ToString());
        }

        private void nudPrice_ValueChanged(object sender, EventArgs e)
        {
            UpdateTotals();
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            dgvProducts.Rows.Add(txtProductName.Text, cmbCategory.Text, nudPrice.Value, nudQuantity.Value, DateTime.Now);
            UpdateTotals();
            ClearFields();
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            if (dgvProducts.CurrentRow != null)
            {
                dgvProducts.CurrentRow.Cells[0].Value = txtProductName.Text;
                dgvProducts.CurrentRow.Cells[1].Value = cmbCategory.Text;
                dgvProducts.CurrentRow.Cells[2].Value = nudPrice.Value;
                UpdateTotals();
            }
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            if (dgvProducts.CurrentRow != null && MessageBox.Show("Delete?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
                dgvProducts.Rows.Remove(dgvProducts.CurrentRow);
                UpdateTotals();
            }
        }

        private void btnExport_Click(object sender, EventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog();
            sfd.Filter = "CSV|*.csv";
            if (sfd.ShowDialog() == DialogResult.OK)
            {
                using (var writer = new System.IO.StreamWriter(sfd.FileName))
                {
                    foreach (DataGridViewRow row in dgvProducts.Rows)
                        writer.WriteLine(string.Join(",", row.Cells.Cast<DataGridViewCell>().Select(c => c.Value)));
                }
            }
        }

        private void txtSearch_TextChanged(object sender, EventArgs e)
        {
            foreach (DataGridViewRow row in dgvProducts.Rows)
            {
                row.Visible = row.Cells[0].Value?.ToString().Contains(txtSearch.Text, StringComparison.OrdinalIgnoreCase) ?? false;
            }
        }

        private void chkLowStock_Changed(object sender, EventArgs e)
        {
            foreach (DataGridViewRow row in dgvProducts.Rows)
            {
                if (chkLowStock.Checked)
                    row.Visible = Convert.ToInt32(row.Cells[3].Value) < 10;
                else
                    row.Visible = true;
            }
        }

        private void autoRefreshTimer_Tick(object sender, EventArgs e)
        {
            UpdateTotals();
            lblTotal.Text = $"Total: {dgvProducts.Rows.Count} items";
        }
    }
}