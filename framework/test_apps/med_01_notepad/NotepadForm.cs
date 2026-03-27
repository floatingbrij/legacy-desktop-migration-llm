using System;
using System.Windows.Forms;
using System.Drawing;

namespace SimpleNotepad
{
    public partial class NotepadForm : Form
    {
        public NotepadForm()
        {
            InitializeComponent();
        }

        private void rtbEditor_TextChanged(object sender, EventArgs e)
        {
            lblStatus.Text = $"Characters: {rtbEditor.Text.Length}";
        }

        private void btnNew_Click(object sender, EventArgs e)
        {
            if (MessageBox.Show("New document?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)
                rtbEditor.Text = "";
        }

        private void btnOpen_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "Text files|*.txt";
            if (ofd.ShowDialog() == DialogResult.OK)
                rtbEditor.Text = System.IO.File.ReadAllText(ofd.FileName);
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog();
            sfd.Filter = "Text files|*.txt";
            if (sfd.ShowDialog() == DialogResult.OK)
                System.IO.File.WriteAllText(sfd.FileName, rtbEditor.Text);
        }

        private void cmbFontSize_Changed(object sender, EventArgs e)
        {
            float size = float.Parse(cmbFontSize.SelectedItem.ToString());
            rtbEditor.Font = new System.Drawing.Font(rtbEditor.Font.FontFamily, size);
        }

        private void chkWordWrap_Changed(object sender, EventArgs e)
        {
            rtbEditor.WordWrap = chkWordWrap.Checked;
        }
    }
}