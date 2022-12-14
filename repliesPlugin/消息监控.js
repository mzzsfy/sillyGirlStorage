//插件功能:消息监控,自定义ban人,按时间禁用等功能
//[rule: ?] 匹配所有消息
//[priority: 9999999999999999999]
//[imType:qq]
//[show:消息管理]
//[enable: true] //是否禁用本插件

let config = {
    log: false,
    message: {
        enable: false,
        //默认禁言时间,单位秒,最少1分钟
        banTime: 60,
        //默认禁言是否通知
        banNotify: false,
        //默认踢人是否通知
        kickNotify: true,
        //撤回是否通知
        recallNotify: false,
        //撤回后是否允许傻妞其他插件继续匹配
        recallContinue: false,
        //相关规则
        rules: {
            "这里填写需要匹配的词1": {
                //是否踢出群,默认不踢
                kick: true,
                //踢出时是否拉黑名单
                reject: true,
                //踢出时是否通知傻妞的管理
                kickNotify: true,
                //包含的类型
                imType: ["qq"],
                //回复
                reply: "恭喜获取永久飞机票一张"
            },
            "这里填写需要匹配的词2": {
                //禁言一小时
                banTime: 3600,
                //ban是否通知傻妞的管理
                banNotify: true,
                reply: "恭喜获取一小时禁言套餐"
            },
            //撤回群里的手机号,并按使用默认配置禁言一分钟,不禁言设置disableBan:true
            "/1\\d{10}/": {
                //是否禁用禁言功能,禁用后只执行撤回
                //disableBan: true,
                //是否撤回
                recall: true,
                //撤回是否通知
                // recallNotify: false,
                //是否仅群聊有效
                onlyGroup: true,
                //生效的群id
                // groupId: [],
                //撤回后是否允许继续处理
                //recallContinue: false,
            },
            //使用默认配置
            "这里填写需要匹配的词3": {},
            //使用正则匹配,使用默认配置
            "/这里填写需要匹配的正则表达式1/": {},
            //使用正则匹配,使用默认配置
            "/这里填写需要匹配的正则表达式2/": {},
        }
    },
    //分时段禁用
    timeDisable: {
        enable: true,
        //规则:
        //从00:00:00点开始匹配,23:59:59结束
        //当匹配成功后取最后成功匹配的规则
        times: [{
            time: "00:00:00",
            //启用
            enable: true,
            //是否允许管理员
            admin: true,
            //是否允许私聊
            privateChat: false,
            //是否允许群聊
            groupChat: true,
            //匹配特定的条件,允许正则
            // text: ["查询"],
            //白名单条件,允许正则
            whitelistText: ['/pt_key=[\\w\\-_%]+;pt_pin=[\\w\\-_%]+;/'],
            //匹配特定的im
            imType: ["qq"],
            //白名单用户,要字符串,类似["88888","10000"]
            // whitelistUser:[],
            //白名单群,要字符串,类似["88888","10000"]
            // whitelistGroup:[],
            //回复,选填
            // reply: "不允许私聊",
        }, /*{
            time: "23:59:59",
            enable: false
        }, */]
    },
}

let now = new Date()
let nowString = call('now')

function main() {
    if (
        doLog() &&
        message() &&
        timeDisable()
    ) {
        Continue()
    }
}

//记录日志
function doLog() {
    if (config.log) {
        console.log(`${nowString},${GetUsername()}(${GetUserID()})在${ImType()}:${GetChatname()}:${GetChatID()}发送消息:${GetContent()}`)
    }
    return true
}

//禁言
function message() {
    if (config.message.enable) {
        let rules = config.message.rules
        for (let text in rules) {
            let conf = rules[text]
            if (conf.imType && conf.imType.length > 0 && !conf.imType.includes(ImType())) {
                continue
            }
            if (!GetChatID() && conf.onlyGroup){
                continue
            }
            if (match(text,GetContent())) {
                if(!conf.disableBan){
                    let kick = conf.kick
                    let notify = kick ?
                        (conf.kickNotify || config.message.kickNotify) :
                        (conf.banNotify || config.message.banNotify);
                    //是否在群里,不在群里只判断通知逻辑
                    if (GetChatID()) {
                        if (kick) {
                            GroupKick(GetUserID(), !!conf.reject)
                        } else {
                            GroupBan(GetUserID(), conf.banTime || config.message.banTime)
                        }
                        if (conf.reply) {
                            sendText(conf.reply)
                        }
                    }
                    if (notify) {
                        notifyMasters(`${nowString}在${ImType()}因为${GetContent()}${kick?"踢出":("禁言"+(conf.banTime || config.message.banTime)+"秒")}:${GetUsername()}(${GetUserID()}),在群:${GetChatname()}:${GetChatID()}`)
                    }
                }
                //撤回逻辑
                if (conf.recall){
                    Delete()
                    return config.recallContinue === undefined?config.message.recallContinue:config.recallContinue
                }
                return false
            }
        }
    }
    return true
}
//按时间禁用功能
function timeDisable() {
    if (config.timeDisable.enable) {
        let times = config.timeDisable.times
        let last = {
            enable: false
        }
        for (let t of times) {
            let testDate = new Date("2000-01-01 " + t.time)
            if (
                now.getHours() >= testDate.getHours() &&
                now.getMinutes() >= testDate.getMinutes() &&
                now.getSeconds() >= testDate.getSeconds()
            ) {
                last = t
            } else {
                break
            }
        }
        if (last.enable) {
            if (last.imType && last.imType.length > 0) {
                if (!last.imType.includes(ImType())) {
                    return true
                }
            }
            if (last.text && last.text.length > 0) {
                let m = false
                for (let t of last.text) {
                    if (match(t,GetContent())) {
                        m = true
                        break
                    }
                }
                if (!m) {
                    return true
                }
            }
            if(last.admin&&isAdmin()){
                return true
            }
            if(last.whitelistUser&&last.whitelistUser.length>0&&last.whitelistUser.indexOf(""+GetUserID())>-1){
                return true
            }
            if(last.whitelistGroup&&last.whitelistGroup.length>0&&last.whitelistGroup.indexOf(""+GetChatID())>-1){
                return true
            }
            if (GetChatID()) {
                if (last.groupChat) {
                    return true
                }
            } else {
                if (last.privateChat) {
                    return true
                }
            }
            if (last.reply) {
                sendText(last.reply)
            }
            if (last.whitelistText && last.whitelistText.length > 0) {
                for (let t of last.whitelistText) {
                    if (match(t,GetContent())) {
                        return true
                    }
                }
            }
            return false
        }
    }
    return true
}

function match(rule, text) {
    if (rule.startsWith("/") && rule.endsWith("/")) {
        return new RegExp(rule.substring(1, rule.length - 1)).test(text)
    } else {
        return text.includes(rule)
    }
}

main()
