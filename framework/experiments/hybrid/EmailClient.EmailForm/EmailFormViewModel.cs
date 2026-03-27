using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace EmailClient
{
    public partial class EmailFormViewModel : ObservableObject
    {
        [ObservableProperty]
        private DateTime _lvEmailsValue;

        [ObservableProperty]
        private string _txtSearchValue;

        [RelayCommand]
        private async Task lvEmailsDoubleClickAsync()
        {
            if (lvEmails.SelectedItems.Count > 0)
            {
            var compose = new ComposeForm((Email)lvEmails.SelectedItems[0].Tag);
            compose.ShowDialog();
            }
        }

        [RelayCommand]
        private async Task btnComposeAsync()
        {
            var compose = new ComposeForm();
            compose.ShowDialog();
        }

        [RelayCommand]
        private async Task btnReplyAsync()
        {
            if (lvEmails.SelectedItems.Count > 0)
            new ComposeForm((Email)lvEmails.SelectedItems[0].Tag, ComposeMode.Reply).ShowDialog();
        }

        [RelayCommand]
        private async Task btnForwardAsync()
        {
            new ComposeForm(null, ComposeMode.Forward).ShowDialog();
        }

        [RelayCommand]
        private async Task btnDeleteAsync()
        {
            if (lvEmails.SelectedItems.Count > 0 && await ShowDialogAsync("Delete email?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
            lvEmails.Items.Remove(lvEmails.SelectedItems[0]);
            lblStatusText = $"Inbox ({lvEmails.Items.Count} messages)";
            }
        }

        [RelayCommand]
        private async Task btnRefreshAsync()
        {
            progressBar1IsVisible = true;
            BackgroundWorker bw = new BackgroundWorker();
            bw.DoWork += (s, ev) => { Thread.Sleep(2000); };
            bw.RunWorkerCompleted += (s, ev) => { this.Invoke((Action)(() => { LoadFolder("Inbox"); progressBar1IsVisible = false; })); };
            bw.RunWorkerAsync();
        }

    }
}