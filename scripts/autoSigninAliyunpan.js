/**
 * @name autoSignin.js
 * @author Anonym-w
 * @version 0.1
 */

const scriptName = "阿里云盘签到";
const updateAccesssTokenURL = "https://auth.aliyundrive.com/v2/account/token"
const signinURL = "https://member.aliyundrive.com/v1/activity/sign_in_list"
let allMessage = ``;
let Msg0 = ""
/*#const refreshTokenArray = [
    "",
    ""
    ]*/
refreshTokenArray = process.env.Aliyunpan_refleshToken.split('&')
if (!refreshTokenArray.length) {
	console.log('未获取到refreshToken, 程序终止')
	process.exit(1)
}
const fetch = require("node-fetch")
const notify = require('./sendNotify');

!(async () => {
	for (const elem of refreshTokenArray) {
		index = 1
		
		const queryBody = {
			'grant_type': 'refresh_token',
			'refresh_token': elem
		};

		//使用 refresh_token 更新 access_token
		fetch(updateAccesssTokenURL, {
				method: "POST",
				body: JSON.stringify(queryBody),
				headers: {
					'Content-Type': 'application/json'
				}
			})
			.then((res) => res.json())
			.then((json) => {
				//console.log('***************1**********')
				//console.log(json);

				let access_token = json.access_token;
				let nick_name = json.nick_name;
				//console.log(access_token);

				//签到

				fetch(signinURL, {
						method: "POST",
						body: JSON.stringify(queryBody),
						headers: {
							'Authorization': 'Bearer ' + access_token,
							'Content-Type': 'application/json'
						}
					})
					.then((res) => res.json())
					.then((json) => {
						//console.log(json);
						//console.log(nick_name + ":");
						Msg0 = Msg0 + nick_name + ":"
						allMessage = allMessage + nick_name + `:`

						if (!json.success) {
							console.log('签到失败')
							Msg0 = Msg0 + `签到失败\n`
							allMessage = allMessage + `签到失败\n`                            
						}

						//console.log('签到成功')
						Msg0 = Msg0 + "签到成功\n"
						allMessage = allMessage + `签到成功\n`

						const {
							signInLogs,
							signInCount
						} = json.result
						const currentSignInfo = signInLogs[signInCount - 1] // 当天签到信息
						//console.log(currentSignInfo.reward)
						//console.log(currentSignInfo.reward.name)
						//console.log(currentSignInfo.reward.description)
						if (currentSignInfo.reward) {
							Msg0 = Msg0 + `本次签到获得 ${currentSignInfo.reward.name} \n`
							allMessage = allMessage + `本次签到获得 ${currentSignInfo.reward.name} \n`                            
						}


						//console.log(`本月累计签到 ${signInCount} 天`)
						Msg0 = Msg0 + `本月累计签到 ${signInCount} 天\n`
						allMessage = allMessage + `本月累计签到 ${signInCount} 天\n`
                        //console.log(allMessage)

						//console.log('****************')
						Msg0 = Msg0 + '***************************'						
						//console.log('------------')
						//notify.sendNotify(`阿里云盘签到结果`,Msg0)
						allMessage = allMessage + `********\n`
                        console.log(allMessage)
                        //notify.sendNotify(`阿里云盘签到结果`,allMessage)                         

					})
					.catch((err) => console.log(err))
                
				  
			})
			.catch((err) => console.log(err))

	}

	//await notify.sendNotify(`阿里云盘签到结果`,allMessage)


})()
.catch((e) => {
		console.error(`❗️  运行错误！\n${e}`)
	})
	.finally()
//console.log(allMessage)     
// notify.sendNotify(`阿里云盘签到结果`,allMessage)
// notify.sendNotify(`v2free 自动签到结果`,allnotify)