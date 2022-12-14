// [rule:export ?=?]
// [admin: true]
// [priority: -100]
// [show: export直接生效]

function main(){
    GetContent()
    .split('\n')
    .map(s=>s.trim())
    .filter(s=>!s.startsWith('#'))
    .forEach(s=>{
        let res = /export ([a-z_\-0-9]+)=(?:"|')?([^#\s'"]+)(?:"|')?/ig.exec(s)
        // sendText(`尝试解析${s},结果${JSON.stringify(res)}`)
        if (res){
            let r=`ql env set ${res[1]} ${res[2]}`
            sendText("已转换并执行: "+r)
            sleep(100)
            breakIn(r)
        }
    })
}

main()