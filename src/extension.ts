import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { webcrypto } from 'crypto';

export function activate(context: vscode.ExtensionContext) {
	// 注册侧边栏 Webview
    const provider = new SidebarWebviewProvider(context.extensionUri);
	context.subscriptions.push(
		    vscode.window.registerWebviewViewProvider(
				'pris718_activitybar.sidebarView', // 与 package.json 中视图ID一致
				provider,
				{ webviewOptions: { retainContextWhenHidden: false } }
        )
    );

	//注册command
	const disposable = registerCommand(context);
	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}

const DFT_CHECK_URL = "http://10.10.90.248:5000/check";
const SCHOOL_LIST_GPU_USAGE_URL = "http://10.160.4.55:5000/api/list_gpu_usage/school";
const GET_HOST_LIST_URL = "http://10.160.4.55:5000/api/host_list/dft"
const DFT_LIST_GPU_USAGE_URL = "http://10.10.90.248:5000/api/gpu_usage_by_list"

async function getGpuList(): Promise<Object> {
    // 获取school的数据
    const apiUrl = SCHOOL_LIST_GPU_USAGE_URL;
    var school_json = [];
	try {
        // 发起GET请求
        const response = await fetch(apiUrl);
        
        // 检查请求是否成功（状态码200-299）
        if (!response.ok) {
            throw new Error(`请求失败，状态码: ${response.status}`);
        }
        // 解析响应数据（根据后端返回格式调整，这里以JSON为例）
        const data = await response.json();
        // 处理数据并返回（根据实际需求调整）
        school_json = JSON.parse(JSON.stringify(data))
    } catch (error) {
        console.error("校园网服务器访问失败！");
    }
    
    // 获取dft的数据，先访问check接口判断是否能连上服务器
    try{
        var response = await fetchWithTimeout(DFT_CHECK_URL, {
        method: "GET"
        }, 2000);
        if (response instanceof Response && !response.ok) {
            console.error("东方通服务器访问失败！");
            return school_json;
        }
    } catch (error) {
        console.error("东方通服务器访问失败！");
        return school_json;
    }
    

    var dft_json = []
    const controller = new AbortController()
    try {
        // 发起GET请求
        var response = await fetchWithTimeout(GET_HOST_LIST_URL, {
            method: "GET"
        });
        // 检查请求是否成功（状态码200-299）
        if (response instanceof Response && !response.ok) {
            throw new Error(`请求失败，状态码: ${response.status}`);
        }
        if (!(response instanceof Response)) {
            throw new Error('Unexpected response type');
        }
        // 解析响应数据（根据后端返回格式调整，这里以JSON为例）
        var data = await response.json();
        // 处理数据并返回（根据实际需求调整）
        var host_list = data
        response = await fetchWithTimeout(DFT_LIST_GPU_USAGE_URL, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(host_list)
        })
        setTimeout(() => {
            console.log(controller)
            controller.abort()
          }, 10000)
        if (!(response instanceof Response)) {
            throw new Error('Unexpected response type');
        }
        data = await response.json();
        dft_json = JSON.parse(JSON.stringify(data))
    } catch (error) {
        console.error("东方通服务器访问失败！");
    }
    return [...school_json, ...dft_json]
}

function registerCommand(context: vscode.ExtensionContext) {
	return vscode.commands.registerCommand('pris.pris718', () => {
		const panel = vscode.window.createWebviewPanel(
            'index',
            'pris-718服务器',
            vscode.ViewColumn.Active,
            {
                enableScripts: true,
                localResourceRoots: [
                    vscode.Uri.file(path.join(context.extensionPath, 'src'))
                ]
            }
        );

		//vscode.window.showInformationMessage('pris-718服务器系统');

		//读html文件
		const htmlPath = path.join(context.extensionPath, 'src', 'webview', 'index.html');
		const htmlContent = fs.readFileSync(htmlPath, 'utf8');
		panel.webview.html = htmlContent;

		// 监听webview消息
		panel.webview.onDidReceiveMessage(
			async(message) => {
				if (message.command === 'getGpuList') {
					const result = await getGpuList();
					panel.webview.postMessage(result);
				}
			},
			undefined,
			context.subscriptions
		);
	});
}

function fetchWithTimeout(url: string, options: any, timeout = 10000) {
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => {
        reject(new Error('Request timeout'));
      }, timeout);
    });
    return Promise.race([
      fetch(url, options),
      timeoutPromise
    ]);
}

// 侧边栏 Webview 提供者类
class SidebarWebviewProvider implements vscode.WebviewViewProvider {
    private _webviewView?: vscode.WebviewView;
    private _extensionUri: vscode.Uri;

    constructor(extensionUri: vscode.Uri) {
		console.log("运行路径：" + extensionUri);
        this._extensionUri = extensionUri;
    }

    // 当侧边栏视图被创建/显示时触发
    public resolveWebviewView(webviewView: vscode.WebviewView) {
		console.log("Side bar event hits.");

        this._webviewView = webviewView;

        // 配置 Webview 权限
        webviewView.webview.options = {
            enableScripts: true,
            // 允许访问插件内的本地资源（如 HTML、CSS）
            localResourceRoots: [
                vscode.Uri.joinPath(this._extensionUri, 'src', 'webview')
            ]
        };
        // 读取单独的 HTML 文件并设置到 Webview
        const htmlPath = path.join(
            this._extensionUri.fsPath,
            'src',
            'webview',
            'index.html'
        );
        const htmlContent = fs.readFileSync(htmlPath, 'utf-8');
        webviewView.webview.html = htmlContent;
        // 监听 Webview 发送的消息
        webviewView.webview.onDidReceiveMessage(
            async (message) => {
                console.log(message.command);
                if (message.command === 'getGpuList') {
                    // 发起 GET 请求
                    const result = await getGpuList();
                    // 发送结果回 Webview
                    this._webviewView?.webview.postMessage(result);
                }
            },
            undefined
        );
    }
}

