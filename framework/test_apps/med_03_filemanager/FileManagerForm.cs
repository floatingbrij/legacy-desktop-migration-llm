using System;
using System.Windows.Forms;
using System.Drawing;

namespace FileManagerApp
{
    public partial class FileManagerForm : Form
    {
        public FileManagerForm()
        {
            InitializeComponent();
        }

        private void tvFolders_AfterSelect(object sender, EventArgs e)
        {
            string path = tvFolders.SelectedNode.Tag.ToString();
            txtPath.Text = path;
            LoadFiles(path);
        }

        private void lvFiles_DoubleClick(object sender, EventArgs e)
        {
            if (lvFiles.SelectedItems.Count > 0)
            {
                string file = lvFiles.SelectedItems[0].Tag.ToString();
                System.Diagnostics.Process.Start(file);
            }
        }

        private void txtPath_KeyDown(object sender, EventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
                LoadPath(txtPath.Text);
        }

        private void btnGo_Click(object sender, EventArgs e)
        {
            LoadPath(txtPath.Text);
        }
    }
}