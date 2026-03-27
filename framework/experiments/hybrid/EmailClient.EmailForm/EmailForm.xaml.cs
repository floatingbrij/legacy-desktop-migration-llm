using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace EmailClient
{
    public sealed partial class EmailForm : Window
    {
        public EmailForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void tvFolders_AfterSelect(object sender, RoutedEventArgs e)
        {
            LoadFolder(tvFolders.SelectedNode.Text);
        }

        // Migrated from WinForms event handler
        private void lvEmails_SelectedIndexChanged(object sender, SelectionChangedEventArgs e)
        {
            if (lvEmails.SelectedItems.Count > 0)
                        {
                            var email = (Email)lvEmails.SelectedItems[0].Tag;
                            lblFromValue.Text = email.From;
                            lblSubjectValue.Text = email.Subject;
                            lblDateValue.Text = email.Date.ToString();
                            rtbBody.Text = email.Body;
                        }
        }

        // Migrated from WinForms event handler
        private void lvEmails_DoubleClick(object sender, RoutedEventArgs e)
        {
            if (lvEmails.SelectedItems.Count > 0)
                        {
                            var compose = new ComposeForm((Email)lvEmails.SelectedItems[0].Tag);
                            compose.ShowDialog();
                        }
        }

        // Migrated from WinForms event handler
        private void btnCompose_Click(object sender, RoutedEventArgs e)
        {
            var compose = new ComposeForm();
                        compose.ShowDialog();
        }

        // Migrated from WinForms event handler
        private void btnReply_Click(object sender, RoutedEventArgs e)
        {
            if (lvEmails.SelectedItems.Count > 0)
                            new ComposeForm((Email)lvEmails.SelectedItems[0].Tag, ComposeMode.Reply).ShowDialog();
        }

        // Migrated from WinForms event handler
        private void btnForward_Click(object sender, RoutedEventArgs e)
        {
            new ComposeForm(null, ComposeMode.Forward).ShowDialog();
        }

        // Migrated from WinForms event handler
        private void btnDelete_Click(object sender, RoutedEventArgs e)
        {
            if (lvEmails.SelectedItems.Count > 0 && await ShowDialogAsync("Delete email?", "Confirm", MessageBoxButtons.YesNo) == ContentDialogResult.Yes)
                        {
                            lvEmails.Items.Remove(lvEmails.SelectedItems[0]);
                            lblStatus.Text = $"Inbox ({lvEmails.Items.Count} messages)";
                        }
        }

        // Migrated from WinForms event handler
        private void btnRefresh_Click(object sender, RoutedEventArgs e)
        {
            progressBar1.Visibility = Visibility.Visible;
                        BackgroundWorker bw = new BackgroundWorker();
                        bw.DoWork += (s, ev) => { Thread.Sleep(2000); };
                        bw.RunWorkerCompleted += (s, ev) => { this.Invoke((Action)(() => { LoadFolder("Inbox"); progressBar1.Visibility = Visibility.Collapsed; })); };
                        bw.RunWorkerAsync();
        }

        // Migrated from WinForms event handler
        private void txtSearch_TextChanged(object sender, TextChangedEventArgs e)
        {
            foreach (ListViewItem item in lvEmails.Items)
                            item.Background = new SolidColorBrush(item.Text.Contains(txtSearch.Text) ? System.Drawing.Color.Yellow : System.Drawing.Color.White;
        }

        // Migrated from WinForms event handler
        private void checkMailTimer_Tick(object sender, object e)
        {
            CheckNewMail();
                        lblStatus.Text = $"Last check: {DateTime.Now:HH:mm:ss}";
        }
    }
}