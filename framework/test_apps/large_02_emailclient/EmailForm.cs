using System;
using System.Windows.Forms;
using System.Drawing;

namespace EmailClient
{
    public partial class EmailForm : Form
    {
        public EmailForm()
        {
            InitializeComponent();
        }

        private void tvFolders_AfterSelect(object sender, EventArgs e)
        {
            LoadFolder(tvFolders.SelectedNode.Text);
        }

        private void lvEmails_SelectedIndexChanged(object sender, EventArgs e)
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

        private void lvEmails_DoubleClick(object sender, EventArgs e)
        {
            if (lvEmails.SelectedItems.Count > 0)
            {
                var compose = new ComposeForm((Email)lvEmails.SelectedItems[0].Tag);
                compose.ShowDialog();
            }
        }

        private void btnCompose_Click(object sender, EventArgs e)
        {
            var compose = new ComposeForm();
            compose.ShowDialog();
        }

        private void btnReply_Click(object sender, EventArgs e)
        {
            if (lvEmails.SelectedItems.Count > 0)
                new ComposeForm((Email)lvEmails.SelectedItems[0].Tag, ComposeMode.Reply).ShowDialog();
        }

        private void btnForward_Click(object sender, EventArgs e)
        {
            new ComposeForm(null, ComposeMode.Forward).ShowDialog();
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            if (lvEmails.SelectedItems.Count > 0 && MessageBox.Show("Delete email?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
                lvEmails.Items.Remove(lvEmails.SelectedItems[0]);
                lblStatus.Text = $"Inbox ({lvEmails.Items.Count} messages)";
            }
        }

        private void btnRefresh_Click(object sender, EventArgs e)
        {
            progressBar1.Visible = true;
            BackgroundWorker bw = new BackgroundWorker();
            bw.DoWork += (s, ev) => { Thread.Sleep(2000); };
            bw.RunWorkerCompleted += (s, ev) => { this.Invoke((Action)(() => { LoadFolder("Inbox"); progressBar1.Visible = false; })); };
            bw.RunWorkerAsync();
        }

        private void txtSearch_TextChanged(object sender, EventArgs e)
        {
            foreach (ListViewItem item in lvEmails.Items)
                item.BackColor = item.Text.Contains(txtSearch.Text) ? System.Drawing.Color.Yellow : System.Drawing.Color.White;
        }

        private void checkMailTimer_Tick(object sender, EventArgs e)
        {
            CheckNewMail();
            lblStatus.Text = $"Last check: {DateTime.Now:HH:mm:ss}";
        }
    }
}