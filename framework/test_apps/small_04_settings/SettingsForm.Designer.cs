namespace SettingsApp
{
    partial class SettingsForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.lblTheme = new System.Windows.Forms.Label();
            this.cmbTheme = new System.Windows.Forms.ComboBox();
            this.chkAutoSave = new System.Windows.Forms.CheckBox();
            this.chkNotify = new System.Windows.Forms.CheckBox();
            this.btnSave = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // lblTheme
            this.lblTheme.Text = "Theme:";
            this.lblTheme.Location = new System.Drawing.Point(20, 20);
            this.lblTheme.Size = new System.Drawing.Size(80, 20);
            this.lblTheme.Name = "lblTheme";
            // cmbTheme
            this.cmbTheme.Location = new System.Drawing.Point(110, 17);
            this.cmbTheme.Size = new System.Drawing.Size(200, 23);
            this.cmbTheme.Name = "cmbTheme";
            this.cmbTheme.SelectedIndexChanged += new System.EventHandler(this.cmbTheme_SelectedIndexChanged);
            // chkAutoSave
            this.chkAutoSave.Text = "Auto-save";
            this.chkAutoSave.Location = new System.Drawing.Point(20, 60);
            this.chkAutoSave.Size = new System.Drawing.Size(150, 20);
            this.chkAutoSave.Name = "chkAutoSave";
            this.chkAutoSave.CheckedChanged += new System.EventHandler(this.chkAutoSave_CheckedChanged);
            // chkNotify
            this.chkNotify.Text = "Notifications";
            this.chkNotify.Location = new System.Drawing.Point(20, 90);
            this.chkNotify.Size = new System.Drawing.Size(150, 20);
            this.chkNotify.Name = "chkNotify";
            // btnSave
            this.btnSave.Text = "Save";
            this.btnSave.Location = new System.Drawing.Point(120, 180);
            this.btnSave.Size = new System.Drawing.Size(90, 30);
            this.btnSave.Name = "btnSave";
            this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
            // btnCancel
            this.btnCancel.Text = "Cancel";
            this.btnCancel.Location = new System.Drawing.Point(220, 180);
            this.btnCancel.Size = new System.Drawing.Size(90, 30);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);
            // SettingsForm
            this.ClientSize = new System.Drawing.Size(350, 250);
            this.Controls.Add(this.btnCancel);
            this.Controls.Add(this.btnSave);
            this.Controls.Add(this.chkNotify);
            this.Controls.Add(this.chkAutoSave);
            this.Controls.Add(this.cmbTheme);
            this.Controls.Add(this.lblTheme);
            this.Name = "SettingsForm";
            this.Text = "Settings";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Label lblTheme;
        private System.Windows.Forms.ComboBox cmbTheme;
        private System.Windows.Forms.CheckBox chkAutoSave;
        private System.Windows.Forms.CheckBox chkNotify;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.Button btnCancel;
    }
}