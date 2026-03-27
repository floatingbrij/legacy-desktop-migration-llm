using System;
using System.Windows.Forms;
using System.Drawing;

namespace SettingsApp
{
    public partial class SettingsForm : Form
    {
        public SettingsForm()
        {
            InitializeComponent();
        }

        private void cmbTheme_SelectedIndexChanged(object sender, EventArgs e)
        {
            lblTheme.Text = "Theme: " + cmbTheme.SelectedItem.ToString();
        }

        private void chkAutoSave_CheckedChanged(object sender, EventArgs e)
        {
            if (chkAutoSave.Checked) { /* enable */ }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Settings saved!"); this.Close();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}