function emailV(email) {
    const emailV = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
    if (!emailV.test(email)) {
        toastr.warning('亲爱哒，邮箱格式不正确哦！')
        return false
    }
    if (!email) {
        toastr.warning('亲爱哒，请先输入邮箱哦！')
        return false
    }
    return true

}

function captchaV(captcha) {
    if (captcha.length === 6) {
        return true
    } else {
        toastr.warning('亲爱哒，验证码错误哦！')
        return false
    }
}

function usernameV(username) {
    if (username.length < 1 || username.length > 5) {
        toastr.error('亲爱哒，用户名长度应该在1-5位之间哦！')
        return false
    } else {
        return true
    }
}

function pwdV(pwd) {
    if (7 > pwd.length || pwd.length > 21) {
        toastr.error('亲爱哒，密码长度应该在6-20位之间哦！')
        return false
    } else {
        return true
    }

}

function getCaptcha($this, account) {
    if (!usernameV(account)) {
        return
    }
    $.ajax({
        url: '/captcha', method: 'post', data: {
            'account': account
        }, success: function (res) {
            let code = res.code
            if (code === 200) {
                $this.off('click');
                let countSecond = 60
                let timer = setInterval(function () {
                    countSecond -= 1
                    if (countSecond > 0) {
                        $this.text(countSecond + 's')
                    } else {
                        $this.text('Get Code')
                        bindCaptchaBtnClick()
                        clearInterval(timer)
                    }
                }, 1000)
                toastr.success('亲爱哒，验证码发送成功！')
            } else if (code === 400) {
                toastr.warning(res.message)
            } else {
                toastr.error('亲爱哒，该错误暂时无法分析。请联系管理员，错误代码：100001_018！')
            }
        }
    })
}

function getRegisterCaptcha($this, email) {
    if (!emailV(email)) {
        return
    }
    $.ajax({
        url: '/user/registerCaptcha', method: 'post', data: {
            'email': email
        }, success: function (res) {
            let code = res.code
            if (code === 200) {
                $this.off('click');
                let countSecond = 60
                let timer = setInterval(function () {
                    countSecond -= 1
                    if (countSecond > 0) {
                        $this.text(countSecond + 's')
                    } else {
                        $this.text('Get Code')
                        bindCaptchaBtnClick()
                        clearInterval(timer)
                    }
                }, 1000)
                toastr.success('亲爱哒，验证码发送成功！')
            } else if (code === 400) {
                toastr.warning(res.message)
            } else {
                toastr.error('亲爱哒，该错误暂时无法分析。请联系管理员，错误代码：100001_018！')
            }

        }
    })
}

function star(id) {
    $.ajax({
        url: '/star', method: 'post', data: {
            'article_id': id
        }, success: function (data) {
            let code = data.code
            if (code === 200) {
                const starNum = document.getElementById('starNum' + id).innerHTML
                document.getElementById('starNum' + id).innerHTML = (parseInt(starNum) + 1).toString()
                toastr.success(data.message)
            } else if (code === 400) {
                toastr.warning(data.message)
            } else {
                toastr.error('亲爱哒，该错误暂时无法分析。请联系管理员，错误代码：100001_019！')
            }
        }
    })
}

function collection(id) {
    $.ajax({
        url: '/collection', method: 'post', data: {
            'article_id': id
        }, success: function (data) {
            let code = data.code
            if (code === 200) {
                const collectionNum = document.getElementById('collectionNum' + id).innerHTML
                document.getElementById('collectionNum' + id).innerHTML = (parseInt(collectionNum) + 1).toString()
                toastr.success(data.message)
            } else if (code === 400) {
                toastr.warning(data.message)
            } else {
                toastr.error('亲爱哒，该错误暂时无法分析。请联系管理员，错误代码：100001_019！')
            }
        }
    })
}

function notstar(id) {
    $.ajax({
        url: '/notstar', method: 'post', data: {
            'article_id': id
        }, success: function (data) {
            let code = data.code
            let starNums;
            if (code === 200) {
                let starNum = document.getElementById('starNum' + id).innerHTML
                if ((parseInt(starNum) - 1) < 0) {
                    starNums = 0
                } else {
                    starNums = parseInt(starNum) - 1
                }
                document.getElementById('starNum' + id).innerHTML = (starNums).toString()
                toastr.success(data.message)
            } else if (code === 400) {
                toastr.warning(data.message)
            } else {
                toastr.error('亲爱哒，该错误暂时无法分析。请联系管理员，错误代码：100001_019！')
            }
        }
    })
}

function cstar(id) {
    $.ajax({
        url: '/cstar', method: 'post', data: {
            'comment_id': id
        }, success: function (data) {
            let code = data.code
            let cstarNums;
            if (code === 200) {
                const cstarNum = document.getElementById('cstarNum' + id).innerHTML
                document.getElementById('cstarNum' + id).innerHTML = (parseInt(cstarNum) + 1).toString()
            } else if (code === 201) {
                let cstarNum = document.getElementById('cstarNum' + id).innerHTML
                if ((parseInt(cstarNum) - 1) < 0) {
                    cstarNums = 0
                } else {
                    cstarNums = parseInt(cstarNum) - 1
                }
                document.getElementById('cstarNum' + id).innerHTML = (cstarNums).toString()
            } else if (code === 400) {
                toastr.warning(data.message)
            } else {
                toastr.error('亲爱哒，该错误暂时无法分析。请联系管理员，错误代码：100001_019！')
            }
        }
    })
}

window.onload = function () {
    const el = document.getElementById("logout");
    if (el) {
        el.onclick = clear;
    }
}

function clear() {
    localStorage.clear();
    sessionStorage.clear()
    toastr.success('退出成功，浏览器缓存已清空！')
}

function CheckKeyword(key) {
    toastr.options = {
        positionClass: "toast-top-right", timeOut: "1000",
    };

    if (key === 'comments') {
        const keyword = document.getElementById("comments").value;
        if (keyword.length < 3) {
            toastr.error("亲爱哒，评论内容不能少于3个字哦！");
            return false;
        } else {
            return true
        }
    }

    if (key === 'delArticle') {
        if (!emailV($("#delArticleForEmail").val())) {
            return false
        } else return captchaV($("#delArticleForEmail_Captcha").val());
    }

    if (key === 'search') {
        const keyword = document.getElementById("keyword").value;
        if (keyword.length < 1) {
            toastr.error("亲爱哒，关键字不能为空哦！");
            return false;
        } else {
            return true
        }
    }
    if (key === 'publish') {
        const title = document.getElementById("title").value;
        const content = document.getElementById("content").value;
        if (title.length < 5) {
            toastr.error('亲爱哒，标题内容不能少于5个字符哦！')
            return false
        }
        if (content.length < 20) {
            toastr.error('亲爱哒，帖子内容不能少于20个字符哦！')
            return false
        }
        if (title.length > 5 && content.length > 20) {
            return true
        } else {
            toastr.error('亲爱哒，请检查输入的内容是否符合规定长度哦！')
            return false
        }
    }
    if (key === 'register') {
        if (!usernameV($("#username").val())) {
            return false
        } else if (!emailV($("#email").val())) {
            return false
        }  else if (!pwdV($("#password").val())) {
            return false
        }
    }

    if (key === 'login') {
        const account = $("#account").val()
        const password = $("#password").val()
        if (!account) {
            toastr.error('亲爱哒，请先输入账号哦！')
            return false
        } else if (!password) {
            toastr.error('亲爱哒，请先输入密码哦！')
            return false
        } else return pwdV(password);
    }
    if (key === 'retrieve_password') {
        if (!emailV($("#email").val())) {
            return false
        } else if (!captchaV($("#captcha").val())) {
            return false
        } else if (!pwdV($("#password").val())) {
            return false
        } else if ($("#password").val() !== $("#password_confirm").val()) {
            toastr.warning('亲爱哒，两次输入新密码不一致哦！')
            return false
        } else return pwdV($("#password_confirm").val());
    }
    if (key === 'logout') {
        if (!usernameV($("#logoutForUsername").val())) {
            return false
        } else if (!emailV($("#logoutForEmail").val())) {
            return false
        } else if (!captchaV($("#logoutForEmail_Captcha").val())) {
            return false
        } else return pwdV($("#logoutForPwd").val());
    }
    if (key === 'changePersonalData') {
        if (!usernameV($("#username").val())) {
            return false
        }
        const emailChange = $("input[name='emailChange']:checked").val();
        if (emailChange === 1 || emailChange === '1') {
            const changeEmailOldAds = $("#changeEmailOldAds").val()
            const changeEmailNewAds = $("#changeEmailNewAds").val()
            if (!emailV(changeEmailOldAds)) {
                return false
            }
            if (!captchaV($("#changeEmailOldAds_captcha").val())) {
                return false
            }
            if (!emailV(changeEmailNewAds)) {
                return false
            }
            if (!captchaV($("#changeEmailNewAds_captcha").val())) {
                return false
            }
            if (changeEmailOldAds === changeEmailNewAds) {
                toastr.warning('亲爱哒，新旧邮箱不能相同哦！')
                return false
            }
        }

        const signature = $("#signature").val()
        if (signature.length > 20) {
            toastr.warning('亲爱哒，个性签名不能超过20个字！')
            return false
        }
        const contactInformation = $("#contactInformation").val()
        const pwdChange = $("input[name='pwdChange']:checked").val();
        const verifyPwdChange = $("input[name='verifyPwdChange']:checked").val();

        const changePwdForEmail = $("#changePwdForEmail").val()
        const changePwdForEmail_Captcha = $("#changePwdForEmail_Captcha").val()
        const changePwdForEmai_NewPwd = $("#changePwdForEmai_NewPwd").val()
        const changePwdForEmai_RNewPwd = $("#changePwdForEmai_RNewPwd").val()

        const changePwdForPwd_OldPwd = $("#changePwdForPwd_OldPwd").val()
        const changePwdForPwd_NewPwd = $("#changePwdForPwd_NewPwd").val()
        const changePwdForPwd_CNewPwd = $("#changePwdForPwd_CNewPwd").val()

        if (pwdChange === 1 || pwdChange === '1') {
            if (verifyPwdChange === 1 || verifyPwdChange === '1') {
                if (!pwdV(changePwdForPwd_OldPwd)) {
                    return false
                }
                if (!pwdV(changePwdForPwd_NewPwd)) {
                    return false
                }
                if (!pwdV(changePwdForPwd_CNewPwd)) {
                    return false
                }
                if (changePwdForPwd_OldPwd === changePwdForPwd_NewPwd) {
                    toastr.warning('亲爱哒，新旧密码不能相同哦！')
                    return false
                }
                if (changePwdForPwd_CNewPwd !== changePwdForPwd_NewPwd) {
                    toastr.warning('亲爱哒，两次输入新密码不一致哦！')
                    return false
                }
            }
            if (verifyPwdChange === 0 || verifyPwdChange === '0') {
                if (!emailV(changePwdForEmail)) {
                    return false
                }
                if (!captchaV(changePwdForEmail_Captcha)) {
                    return false
                }
                if (!pwdV(changePwdForEmai_NewPwd)) {
                    return false
                }
                if (!pwdV(changePwdForEmai_RNewPwd)) {
                    return false
                }
                if (changePwdForEmai_NewPwd !== changePwdForEmai_RNewPwd) {
                    toastr.warning('亲爱哒，两次输入新密码不一致哦！')
                    return false
                }

            }
        }
    }
}

function bindCaptchaBtnClick() {
    $('#retrieve_captcha_btn').on('click', function (event) {
        event.stopImmediatePropagation();
        getCaptcha($(this), $('input[name="account"]').val())
    });
}

$(function () {
    bindCaptchaBtnClick();
})