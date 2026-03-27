using System;
using System.Windows.Forms;
using System.Drawing;

namespace ContactsManager
{
    public partial class ContactsForm : Form
    {
        public ContactsForm()
        {
            InitializeComponent();
        }

        private void txtName_TextChanged(object sender, EventArgs e)
        {
            btnAdd.Enabled = txtName.Text.Length > 0;
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            ListViewItem item = new ListViewItem(txtName.Text);
            item.SubItems.Add(txtEmail.Text);
            item.SubItems.Add(txtPhone.Text);
            lvContacts.Items.Add(item);
            lblCount.Text = $"{lvContacts.Items.Count} contacts";
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            if (lvContacts.SelectedItems.Count > 0)
            {
                lvContacts.Items.Remove(lvContacts.SelectedItems[0]);
                lblCount.Text = $"{lvContacts.Items.Count} contacts";
            }
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            if (lvContacts.SelectedItems.Count > 0)
            {
                lvContacts.SelectedItems[0].Text = txtName.Text;
                lvContacts.SelectedItems[0].SubItems[1].Text = txtEmail.Text;
            }
        }

        private void lvContacts_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (lvContacts.SelectedItems.Count > 0)
            {
                txtName.Text = lvContacts.SelectedItems[0].Text;
                txtEmail.Text = lvContacts.SelectedItems[0].SubItems[1].Text;
            }
        }

        private void txtSearch_TextChanged(object sender, EventArgs e)
        {
            foreach (ListViewItem item in lvContacts.Items)
            {
                item.BackColor = item.Text.Contains(txtSearch.Text) ? System.Drawing.Color.Yellow : System.Drawing.Color.White;
            }
        }
    }
}