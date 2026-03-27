namespace AboutApp
{
    partial class AboutForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.lblAppName = new System.Windows.Forms.Label();
            this.lblVersion = new System.Windows.Forms.Label();
            this.lblCopyright = new System.Windows.Forms.Label();
            this.btnOK = new System.Windows.Forms.Button();
            this.lnkWebsite = new System.Windows.Forms.LinkLabel();
            this.SuspendLayout();
            // lblAppName
            this.lblAppName.Text = "My Application";
            this.lblAppName.Location = new System.Drawing.Point(50, 20);
            this.lblAppName.Size = new System.Drawing.Size(200, 30);
            this.lblAppName.Font = new System.Drawing.Font("Segoe UI", 14F);
            this.lblAppName.Name = "lblAppName";
            // lblVersion
            this.lblVersion.Text = "Version 1.0.0";
            this.lblVersion.Location = new System.Drawing.Point(50, 60);
            this.lblVersion.Size = new System.Drawing.Size(200, 20);
            this.lblVersion.Name = "lblVersion";
            // lblCopyright
            this.lblCopyright.Text = "(c) 2024 Company";
            this.lblCopyright.Location = new System.Drawing.Point(50, 90);
            this.lblCopyright.Size = new System.Drawing.Size(200, 20);
            this.lblCopyright.Name = "lblCopyright";
            // btnOK
            this.btnOK.Text = "OK";
            this.btnOK.Location = new System.Drawing.Point(100, 130);
            this.btnOK.Size = new System.Drawing.Size(90, 30);
            this.btnOK.Name = "btnOK";
            this.btnOK.Click += new System.EventHandler(this.btnOK_Click);
            // lnkWebsite
            this.lnkWebsite.Text = "www.example.com";
            this.lnkWebsite.Location = new System.Drawing.Point(50, 120);
            this.lnkWebsite.Size = new System.Drawing.Size(200, 20);
            this.lnkWebsite.Name = "lnkWebsite";
            // AboutForm
            this.ClientSize = new System.Drawing.Size(300, 200);
            this.Controls.Add(this.lnkWebsite);
            this.Controls.Add(this.btnOK);
            this.Controls.Add(this.lblCopyright);
            this.Controls.Add(this.lblVersion);
            this.Controls.Add(this.lblAppName);
            this.Name = "AboutForm";
            this.Text = "About";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Label lblAppName;
        private System.Windows.Forms.Label lblVersion;
        private System.Windows.Forms.Label lblCopyright;
        private System.Windows.Forms.Button btnOK;
        private System.Windows.Forms.LinkLabel lnkWebsite;
    }
}