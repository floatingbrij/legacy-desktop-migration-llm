namespace SimpleNotepad
{
    partial class NotepadForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.toolStrip1 = new System.Windows.Forms.ToolStrip();
            this.rtbEditor = new System.Windows.Forms.RichTextBox();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.btnNew = new System.Windows.Forms.Button();
            this.btnOpen = new System.Windows.Forms.Button();
            this.btnSave = new System.Windows.Forms.Button();
            this.lblStatus = new System.Windows.Forms.Label();
            this.cmbFontSize = new System.Windows.Forms.ComboBox();
            this.chkWordWrap = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // menuStrip1
            this.menuStrip1.Dock = DockStyle.Top;
            this.menuStrip1.Name = "menuStrip1";
            // toolStrip1
            this.toolStrip1.Name = "toolStrip1";
            // rtbEditor
            this.rtbEditor.Dock = DockStyle.Fill;
            this.rtbEditor.Name = "rtbEditor";
            this.rtbEditor.TextChanged += new System.EventHandler(this.rtbEditor_TextChanged);
            // statusStrip1
            this.statusStrip1.Dock = DockStyle.Bottom;
            this.statusStrip1.Name = "statusStrip1";
            // btnNew
            this.btnNew.Text = "New";
            this.btnNew.Location = new System.Drawing.Point(10, 50);
            this.btnNew.Size = new System.Drawing.Size(60, 25);
            this.btnNew.Name = "btnNew";
            this.btnNew.Click += new System.EventHandler(this.btnNew_Click);
            // btnOpen
            this.btnOpen.Text = "Open";
            this.btnOpen.Location = new System.Drawing.Point(75, 50);
            this.btnOpen.Size = new System.Drawing.Size(60, 25);
            this.btnOpen.Name = "btnOpen";
            this.btnOpen.Click += new System.EventHandler(this.btnOpen_Click);
            // btnSave
            this.btnSave.Text = "Save";
            this.btnSave.Location = new System.Drawing.Point(140, 50);
            this.btnSave.Size = new System.Drawing.Size(60, 25);
            this.btnSave.Name = "btnSave";
            this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
            // lblStatus
            this.lblStatus.Text = "Ready";
            this.lblStatus.Location = new System.Drawing.Point(10, 420);
            this.lblStatus.Size = new System.Drawing.Size(200, 20);
            this.lblStatus.Name = "lblStatus";
            // cmbFontSize
            this.cmbFontSize.Location = new System.Drawing.Point(220, 50);
            this.cmbFontSize.Size = new System.Drawing.Size(80, 25);
            this.cmbFontSize.Name = "cmbFontSize";
            this.cmbFontSize.SelectedIndexChanged += new System.EventHandler(this.cmbFontSize_Changed);
            // chkWordWrap
            this.chkWordWrap.Text = "Word Wrap";
            this.chkWordWrap.Location = new System.Drawing.Point(310, 52);
            this.chkWordWrap.Size = new System.Drawing.Size(100, 20);
            this.chkWordWrap.Name = "chkWordWrap";
            this.chkWordWrap.CheckedChanged += new System.EventHandler(this.chkWordWrap_Changed);
            // NotepadForm
            this.ClientSize = new System.Drawing.Size(600, 450);
            this.Controls.Add(this.chkWordWrap);
            this.Controls.Add(this.cmbFontSize);
            this.Controls.Add(this.lblStatus);
            this.Controls.Add(this.btnSave);
            this.Controls.Add(this.btnOpen);
            this.Controls.Add(this.btnNew);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.rtbEditor);
            this.Controls.Add(this.toolStrip1);
            this.Controls.Add(this.menuStrip1);
            this.Name = "NotepadForm";
            this.Text = "Notepad";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.RichTextBox rtbEditor;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.Button btnNew;
        private System.Windows.Forms.Button btnOpen;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.Label lblStatus;
        private System.Windows.Forms.ComboBox cmbFontSize;
        private System.Windows.Forms.CheckBox chkWordWrap;
    }
}