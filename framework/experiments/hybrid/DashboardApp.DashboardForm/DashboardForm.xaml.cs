using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace DashboardApp
{
    public sealed partial class DashboardForm : Window
    {
        public DashboardForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void btnDashboard_Click(object sender, RoutedEventArgs e)
        {
            LoadDashboard();
        }

        // Migrated from WinForms event handler
        private void btnReports_Click(object sender, RoutedEventArgs e)
        {
            LoadReports();
        }

        // Migrated from WinForms event handler
        private void btnUsers_Click(object sender, RoutedEventArgs e)
        {
            LoadUsers();
        }

        // Migrated from WinForms event handler
        private void btnSettings_Click(object sender, RoutedEventArgs e)
        {
            var settings = new SettingsForm();
                        settings.ShowDialog();
        }

        // Migrated from WinForms event handler
        private void btnLogout_Click(object sender, RoutedEventArgs e)
        {
            if (await ShowDialogAsync("Logout?", "Confirm", MessageBoxButtons.YesNo) == ContentDialogResult.Yes)
                        {
                            this.Hide();
                            new LoginForm().ShowDialog();
                            this.Close();
                        }
        }

        // Migrated from WinForms event handler
        private void dgvData_CellClick(object sender, RoutedEventArgs e)
        {
            UpdateStats();
        }

        // Migrated from WinForms event handler
        private void dtpStart_Changed(object sender, RoutedEventArgs e)
        {
            FilterByDate();
        }

        // Migrated from WinForms event handler
        private void dtpEnd_Changed(object sender, RoutedEventArgs e)
        {
            FilterByDate();
        }

        // Migrated from WinForms event handler
        private void btnRefresh_Click(object sender, RoutedEventArgs e)
        {
            progressBar1.Value = 0;
                        BackgroundWorker bw = new BackgroundWorker();
                        bw.DoWork += (s, ev) => { for (int i = 0; i <= 100; i += 10) { Thread.Sleep(100); this.Invoke((Action)(() => progressBar1.Value = i)); } };
                        bw.RunWorkerCompleted += (s, ev) => { LoadDashboard(); };
                        bw.RunWorkerAsync();
        }

        // Migrated from WinForms event handler
        private void refreshTimer_Tick(object sender, object e)
        {
            LoadDashboard();
        }

        // Migrated from WinForms event handler
        private void cmbView_Changed(object sender, SelectionChangedEventArgs e)
        {
            ChangeView(cmbView.SelectedItem.ToString());
        }

        // Migrated from WinForms event handler
        private void chkAutoRefresh_Changed(object sender, RoutedEventArgs e)
        {
            refreshTimer.Enabled = chkAutoRefresh.Checked;
        }
    }
}