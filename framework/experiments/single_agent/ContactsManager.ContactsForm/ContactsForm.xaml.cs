using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace ContactsManager
{
    public sealed partial class ContactsForm : Window
    {
        public ContactsForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void txtName_TextChanged(object sender, TextChangedEventArgs e)
        {
            btnAdd.Enabled = txtName.Text.Length > 0;
        }

        // Migrated from WinForms event handler
        private void btnAdd_Click(object sender, RoutedEventArgs e)
        {
            ListViewItem item = new ListViewItem(txtName.Text);
                        item.SubItems.Add(txtEmail.Text);
                        item.SubItems.Add(txtPhone.Text);
                        lvContacts.Items.Add(item);
                        lblCount.Text = $"{lvContacts.Items.Count} contacts";
        }

        // Migrated from WinForms event handler
        private void btnDelete_Click(object sender, RoutedEventArgs e)
        {
            if (lvContacts.SelectedItems.Count > 0)
                        {
                            lvContacts.Items.Remove(lvContacts.SelectedItems[0]);
                            lblCount.Text = $"{lvContacts.Items.Count} contacts";
                        }
        }

        // Migrated from WinForms event handler
        private void btnEdit_Click(object sender, RoutedEventArgs e)
        {
            if (lvContacts.SelectedItems.Count > 0)
                        {
                            lvContacts.SelectedItems[0].Text = txtName.Text;
                            lvContacts.SelectedItems[0].SubItems[1].Text = txtEmail.Text;
                        }
        }

        // Migrated from WinForms event handler
        private void lvContacts_SelectedIndexChanged(object sender, SelectionChangedEventArgs e)
        {
            if (lvContacts.SelectedItems.Count > 0)
                        {
                            txtName.Text = lvContacts.SelectedItems[0].Text;
                            txtEmail.Text = lvContacts.SelectedItems[0].SubItems[1].Text;
                        }
        }

        // Migrated from WinForms event handler
        private void txtSearch_TextChanged(object sender, TextChangedEventArgs e)
        {
            foreach (ListViewItem item in lvContacts.Items)
                        {
                            item.Background = new SolidColorBrush(item.Text.Contains(txtSearch.Text) ? System.Drawing.Color.Yellow : System.Drawing.Color.White;
                        }
        }
    }
}