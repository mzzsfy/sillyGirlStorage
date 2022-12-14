import asyncio
import json
import os
from asyncio import sleep
from pagermaid import persistent_vars, bot, log
from pagermaid.listener import listener
from pagermaid.utils import client, alias_command

"""
Pagermaid sillyGirl plugin.
Silly Gril Repo: https://github.com/cdle/sillyGirl

2022.03.06 refactoring by @mzzsfy
2022.03.09 edit by @mzzsfy
"""
persistent_vars.update(
    {'sillyGirl':
        {
            'self_user_id': 0,
            'secret': '',
            'url': None,
            'whiltelist': set(),
        }
     }
)

@listener(is_plugin=True, outgoing=True, command=alias_command("sillyGirl"), ignore_edited=True, parameters="<message>")
async def sillyGirl(context):
    if context.arguments == 'help' or context.arguments == '?':
        m='''
http://ip:端口  设置傻妞地址
`help`     帮助
`disable`  临时禁用,不带任何参数使用可恢复
`l[ist]`   查看当前白名单,自动撤回
`l[ist]+`  查看当前白名单,不自动撤回
`+`        临时将当前群或回复的消息用户临时加入白名单
`+id`      手动添加临时白名单
`-`        临时将当前群或回复的消息用户临时删除白名单
`-id`      手动临时删除白名单
`save`     保存当前白名单到傻妞
注:临时白名单重启人形后还原
'''
        await context.edit(m)
        return
    if context.arguments == 'disable':
        persistent_vars["sillyGirl"]['url']=''
        await context.edit('已临时禁用傻妞')
        await sleep(3)
        await context.delete()
        return
    if context.arguments == 'save':
        try:
            w='&'.join(persistent_vars["sillyGirl"]['whiltelist'])
            c=await bot.send_message(context.chat_id, f"正在持久化白名单:{w}")
            await sleep(0.5)
            await poll([{
                    'id': c.id,
                    'chat_id': c.chat_id,
                    'text': f"set pgm whiltelist {w}".strip(),
                    'sender_id': c.sender_id,
                    'reply_to': 0,
                    'reply_to_sender_id': 0,
                    'bot_id': persistent_vars["sillyGirl"]['self_user_id'],
                    'is_group': c.is_private == False,
                }])
            await sleep(0.1)
            await c.edit('完成')
            await c.delete()
            await context.edit('持久化完成')
            await sleep(3)
            await context.delete()
        except Exception as e:
            await context.edit(f"持久化白名单失败:{e}")
        return
    if context.arguments.startswith('l'):
        try:
            w='&'.join(persistent_vars["sillyGirl"]['whiltelist'])
            await context.edit(f"当前白名单:{w}")
            if not context.arguments.endswith('+'):
                await sleep(3)
                await context.delete()
        except Exception as e:
            await context.edit(f"获取白名单失败:{e}")
        return
    if context.arguments.startswith('+'):
        try:
            id=0
            if len(context.arguments)>1:
                id=context.arguments[1:]
            else:
                reply = await context.get_reply_message()
                if reply:
                    id=reply.sender_id
                else:
                    id=context.chat_id
            w=persistent_vars["sillyGirl"]['whiltelist']
            w.add(str(id))
            await context.edit(f"已添加临时白名单:{id}")
            await sleep(3)
            await context.delete()
        except Exception as e:
            await context.edit(f"添加临时白名单失败:{e}")
        return
    if context.arguments.startswith('-'):
        try:
            id=0
            if len(context.arguments)>1:
                id=context.arguments[1:]
            else:
                reply = await context.get_reply_message()
                if reply:
                    id=reply.sender_id
                else:
                    id=context.chat_id
            w=persistent_vars["sillyGirl"]['whiltelist']
            w.discard(str(id))
            await context.edit(f"已临时删除白名单:{id}")
            await sleep(3)
            await context.delete()
        except Exception as e:
            await context.edit(f"临时删除白名单失败:{e}")
        return
    if context.arguments and not context.arguments.startswith('http'):
        await context.edit(f"url格式错误,请使用http://xxx格式")
        return
    await context.edit("正在连接到傻妞服务器...")
    await init_url(context)
    async def f(p):
        persistent_vars["sillyGirl"]['whiltelist']=set()
        for reply in p:
            if reply["whiltelist"]:
                persistent_vars["sillyGirl"]['whiltelist'] = set(str(reply["whiltelist"]).split('&'))
                persistent_vars["sillyGirl"]['whiltelist'].discard('')
        if ( not p ) or len(p) <= 0:
            persistent_vars["sillyGirl"]['url']= ''
        else:
            w=persistent_vars["sillyGirl"]['whiltelist']
            await context.edit(f"连接成功")
            await sleep(1)
            await context.delete()
    async def e(e1):
        u=persistent_vars["sillyGirl"]['url']
        persistent_vars["sillyGirl"]['url']=''
        try:
            if u:
                await log(f'连接傻妞失败,url 是不是写错啦? 当前url:{u} 错误: {e}')
                await bot.send_message(persistent_vars["sillyGirl"]['self_user_id'],f'连接傻妞失败,url 是不是写错啦?\n当前url:{u}\n错误: {e}')
                await context.edit(f'连接傻妞失败,详情已发送到收藏夹')
            else:
                await context.edit(f'出现错误,你还没有初始化过url,试试在当前命令后面添加傻妞访问地址,格式http://ip:端口')
        except:
            pass
    try:
        await context.edit("获取白名单中...")
        await poll([],p="?init=true",callback=f,errCallback=e)
    except Exception as e:
        try:
            u=persistent_vars["sillyGirl"]['url']
            persistent_vars["sillyGirl"]['url']=''
            await log(f'连接傻妞失败,url 是不是写错啦? 当前url:{u} 错误: {e}')
            await bot.send_message(persistent_vars["sillyGirl"]['self_user_id'],f'连接傻妞失败,url 是不是写错啦?\n当前url{u}\n错误: {e}')
            await context.edit(f'连接傻妞失败,详情已发送到收藏夹')
        except Exception as e1:
            await log(f"silly_Girl初始化url失败{e1}")

async def init_url(context):
    persistent_vars["sillyGirl"]['url']=''
    if context and context.arguments:
        text = context.arguments
        fd = os.open("sillyGirl.egg", os.O_RDWR | os.O_CREAT | os.O_TRUNC)
        try:
            os.write(fd, bytes(text, 'utf-8'))
        except Exception as e:
            await log(f"持久化url失败{e}")
            if context:
                await context.reply(f"持久化url失败{e}")
        os.close(fd)
    else:
        try:
            fd = os.open("sillyGirl.egg", os.O_RDONLY | os.O_CREAT )
            text = str(os.read(fd, 1200), encoding="utf-8")
            os.close(fd)
            if text is None or text == '':
                if context:
                    await context.edit("请输入正确的地址")
                return
        except Exception as e:
            print(e)
    if '@' in text:
        s1 = text.split("//", 1)
        s2 = s1[1].split("@", 1)
        persistent_vars["sillyGirl"]['secret'] = s2[0]
        text = s1[0]+"//"+s2[1]
    persistent_vars["sillyGirl"]['url'] = text
    await log(f"silly_Girl初始化url成功{text}")


@listener(is_plugin=True, ignore_edited=True)
async def xxx(context):
    text=context.text
    if (text.startswith('-') and ' ' in text ) or text.startswith('**') :
        return
    if not persistent_vars["sillyGirl"]['url'] :
        if persistent_vars["sillyGirl"]['url'] is None:
            await sleep(0.5)
            if not persistent_vars["sillyGirl"]['url']:
                await log('sillyGirl未配置url')
                return
        else:
            return
    if context.sender_id == persistent_vars["sillyGirl"]['self_user_id'] or str(context.sender_id) in persistent_vars["sillyGirl"]['whiltelist'] or str(context.chat_id) in persistent_vars["sillyGirl"]['whiltelist']:
        reply_to = 0
        reply_to = context.id
        reply_to_sender_id = 0
        reply = await context.get_reply_message()
        if reply:
            reply_to = reply.id
            reply_to_sender_id = reply.sender_id
        if ( persistent_vars["sillyGirl"]['self_user_id'] == context.sender_id or context.is_private ):
            reply_to = 0
        try:
            chatId=context.chat_id
            await poll(
                [{
                    'id': context.id,
                    'chat_id': chatId,
                    'text': text,
                    'sender_id': context.sender_id if context.sender_id else -99999999999,
                    'reply_to': reply_to,
                    'reply_to_sender_id': reply_to_sender_id,
                    'bot_id': persistent_vars["sillyGirl"]['self_user_id'],
                    'is_group': context.is_private == False,
                }])
        except Exception as e:
            await log(f'出错了{e}')

async def poll(data,p='',callback=None,errCallback=None):
    replies = await requestToSillGirl(data,p=p,errCallback=errCallback)
    if not replies:
        return
    if callback:
        await callback(replies)
    results = []
    for reply in replies:
        if reply["delete"]:
            try:
                await bot.edit_message(reply["chat_id"], reply["id"], "打错字了，呱呱～")
            except Exception as e:
                pass
            try:
                await bot.delete_messages(reply["chat_id"], [reply["id"]])
            except Exception as e:
                pass
        if reply["id"] != 0:
            try:
                await bot.edit_message(reply["chat_id"], reply["id"], reply["text"])
                continue
            except Exception as e:
                continue
        text = reply["text"]
        images = reply["images"]
        chat_id = reply["chat_id"]
        reply_to = reply["reply_to"]
        context1 = False
        if images and len(images) != 0 :
            async def file(r):
                try:
                    c = await bot.send_file(
                        r["chat_id"],
                        r["images"][0],
                        caption=r["text"],
                        reply_to=r["reply_to"],
                    )
                except Exception as e:
                    await log(f"发送图片错误{e}")
                if c :
                    await poll([{
                        'id': c.id,
                        'uuid': r["uuid"],
                    }])
            asyncio.run_coroutine_threadsafe(file(reply),asyncio.get_event_loop())
        elif text != '':
            context1 = await bot.send_message(chat_id, text, reply_to=reply_to)
        if context1:
            results.append({
                'id': context1.id,
                'uuid': reply["uuid"],
            })
    if len(results):
        await poll(results)


async def requestToSillGirl(data,p='',errCallback=None):
    try:
        req_data = await client.post(persistent_vars["sillyGirl"]['url']+"/pgm"+p, json=data)
    except Exception as e:
        if errCallback:
            return await errCallback(e)
        else:
            raise e
    if not req_data.status_code == 200:
        return
    replies = json.loads(req_data.text)
    return replies



async def _f():
    persistent_vars["sillyGirl"]['self_user_id'] = (await bot.get_me(True)).user_id
    await init_url(None)
    if persistent_vars["sillyGirl"]['url']:
        async def f(p):
            for reply in p:
                if reply["whiltelist"] != "":
                    persistent_vars["sillyGirl"]['whiltelist'] = set(str(reply["whiltelist"]).split('&'))
                    persistent_vars["sillyGirl"]['whiltelist'].discard('')
            w=persistent_vars["sillyGirl"]['whiltelist']
            await log(f"连接成功,当前白名单:{w}")
        async def e(e1):
            u=persistent_vars["sillyGirl"]['url']
            persistent_vars["sillyGirl"]['url']=''
            await log(f'出现错误,url 是不是写错啦?{u}')
        await poll([],p="?init=true",callback=f,errCallback=e)
    while True:
        try:
            if persistent_vars["sillyGirl"]['url']:
                await poll([])
            else:
                await sleep(1)
        except Exception as e:
            # await log(f'出错了:{e}')
            await sleep(0.5)

asyncio.run_coroutine_threadsafe(_f(),asyncio.get_event_loop())
