class LoginForm(Form):

    username = TextField("Username",
                         [validators.Required("사용자명을 입력하세요."),
                          validators.Length(
                              min=4,
                              max=50,
                              message="4자리 이상 50자리 이하로 입력하세요.")
                          ])

    password = PasswordField("NewPassword",
                             [validators.Required("비밀번호를 입력하세요."),
                              validators.Length(
                                  min=4,
                                  max=50,
                                  message="4자리 이상 50자리 이하로 입력하세요."
                              )])

    next_url = HiddenField("Next URL")
