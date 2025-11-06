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

const DFT_URL = "";
const SCHOOL_URL = "";


async function getGpuList(): Promise<Object> {
    const apiUrl = "http://127.0.0.1:5000/api/list_gpu_usage";

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
        return JSON.parse(JSON.stringify(data));
    } catch (error) {
        // 捕获错误（如网络问题、解析失败等）
        return `请求出错: ${error instanceof Error ? error.message : String(error)}`;
    }
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