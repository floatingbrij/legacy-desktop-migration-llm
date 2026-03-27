using System;
using System.Windows.Forms;
using System.Drawing;

namespace DashboardApp
{
    public partial class DashboardForm : Form
    {
        public DashboardForm()
        {
            InitializeComponent();
        }

        private void btnDashboard_Click(object sender, EventArgs e)
        {
            LoadDashboard();
        }

        private void btnReports_Click(object sender, EventArgs e)
        {
            LoadReports();
        }

        private void btnUsers_Click(object sender, EventArgs e)
        {
            LoadUsers();
        }

        private void btnSettings_Click(object sender, EventArgs e)
        {
            var settings = new SettingsForm();
            settings.ShowDialog();
        }

        private void btnLogout_Click(object sender, EventArgs e)
        {
            if (MessageBox.Show("Logout?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
                this.Hide();
                new LoginForm().ShowDialog();
                this.Close();
            }
        }

        private void dgvData_CellClick(object sender, EventArgs e)
        {
            UpdateStats();
        }

        private void dtpStart_Changed(object sender, EventArgs e)
        {
            FilterByDate();
        }

        private void dtpEnd_Changed(object sender, EventArgs e)
        {
            FilterByDate();
        }

        private void btnRefresh_Click(object sender, EventArgs e)
        {
            progressBar1.Value = 0;
            BackgroundWorker bw = new BackgroundWorker();
            bw.DoWork += (s, ev) => { for (int i = 0; i <= 100; i += 10) { Thread.Sleep(100); this.Invoke((Action)(() => progressBar1.Value = i)); } };
            bw.RunWorkerCompleted += (s, ev) => { LoadDashboard(); };
            bw.RunWorkerAsync();
        }

        private void refreshTimer_Tick(object sender, EventArgs e)
        {
            LoadDashboard();
        }

        private void cmbView_Changed(object sender, EventArgs e)
        {
            ChangeView(cmbView.SelectedItem.ToString());
        }

        private void chkAutoRefresh_Changed(object sender, EventArgs e)
        {
            refreshTimer.Enabled = chkAutoRefresh.Checked;
        }
    }
}