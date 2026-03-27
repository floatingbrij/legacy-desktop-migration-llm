using System;
using System.Windows.Forms;

namespace LoginApp
{
    public partial class LoginForm : Form
    {
        public LoginForm() { InitializeComponent(); }

        private void txtUsername_TextChanged(object sender, EventArgs e) { ValidateInputs(); }
        private void txtPassword_TextChanged(object sender, EventArgs e) { ValidateInputs(); }

        private void ValidateInputs()
        {
            btnLogin.Enabled = txtUsername.Text.Length > 0 && txtPassword.Text.Length > 0;
        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            if (txtUsername.Text == "admin" && txtPassword.Text == "password")
            {
                MessageBox.Show("Login successful!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
            else
            {
                MessageBox.Show("Invalid credentials!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                txtPassword.Text = "";
                txtPassword.Focus();
            }
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }
    }
}
