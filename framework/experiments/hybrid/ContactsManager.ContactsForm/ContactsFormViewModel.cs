using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace ContactsManager
{
    public partial class ContactsFormViewModel : ObservableObject
    {
        [ObservableProperty]
        private string _txtNameValue;

        [ObservableProperty]
        private string _lvContactsValue;

        [ObservableProperty]
        private string _txtSearchValue;

        [RelayCommand]
        private void btnAdd()
        {
            ListViewItem item = new ListViewItem(txtNameText);
            item.SubItems.Add(txtEmailText);
            item.SubItems.Add(txtPhoneText);
            lvContacts.Items.Add(item);
            lblCountText = $"{lvContacts.Items.Count} contacts";
        }

        [RelayCommand]
        private void btnDelete()
        {
            if (lvContacts.SelectedItems.Count > 0)
            {
            lvContacts.Items.Remove(lvContacts.SelectedItems[0]);
            lblCountText = $"{lvContacts.Items.Count} contacts";
            }
        }

        [RelayCommand]
        private void btnEdit()
        {
            if (lvContacts.SelectedItems.Count > 0)
            {
            lvContacts.SelectedItems[0].Text = txtNameText;
            lvContacts.SelectedItems[0].SubItems[1].Text = txtEmailText;
            }
        }

    }
}