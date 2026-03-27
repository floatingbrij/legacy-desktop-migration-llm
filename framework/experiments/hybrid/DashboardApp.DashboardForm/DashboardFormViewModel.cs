using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace DashboardApp
{
    public partial class DashboardFormViewModel : ObservableObject
    {
        [ObservableProperty]
        private string _dtpStartValue;

        [ObservableProperty]
        private string _dtpEndValue;

        [ObservableProperty]
        private string _cmbViewValue;

        [ObservableProperty]
        private bool _chkAutoRefreshValue;

        [RelayCommand]
        private void btnDashboard()
        {
            LoadDashboard();
        }

        [RelayCommand]
        private void btnReports()
        {
            LoadReports();
        }

        [RelayCommand]
        private void btnUsers()
        {
            LoadUsers();
        }

        [RelayCommand]
        private async Task btnSettingsAsync()
        {
            var settings = new SettingsForm();
            settings.ShowDialog();
        }

        [RelayCommand]
        private async Task btnLogoutAsync()
        {
            if (await ShowDialogAsync("Logout?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
            this.Hide();
            new LoginForm().ShowDialog();
            this.Close();
            }
        }

        [RelayCommand]
        private async Task btnRefreshAsync()
        {
            progressBar1Value = 0;
            BackgroundWorker bw = new BackgroundWorker();
            bw.DoWork += (s, ev) => { for (int i = 0; i <= 100; i += 10) { Thread.Sleep(100); this.Invoke((Action)(() => progressBar1Value = i)); } };
            bw.RunWorkerCompleted += (s, ev) => { LoadDashboard(); };
            bw.RunWorkerAsync();
        }

    }
}