/*
 * Entrypoint for Dawn's main process
 */

import { app, BrowserWindow, Menu, ipcMain } from 'electron';
/* eslint import/no-extraneous-dependencies: ["error", {"peerDependencies": true}] */
import installExtension, { REACT_DEVELOPER_TOOLS, REDUX_DEVTOOLS } from 'electron-devtools-installer';

import RendererBridge from './RendererBridge';
import { killFakeRuntime } from './MenuTemplate/DebugMenu';
import Template from './MenuTemplate/Template';
import Ansible from './networking/Ansible';
import LCMObject from './networking/FieldControlLCM';

app.on('window-all-closed', () => {
  app.quit();
});

app.on('will-quit', () => {
  Ansible.close();

  if (process.env.NODE_ENV === 'development') {
    killFakeRuntime();
  }
});

function initializeLCM(event) { // eslint-disable-line no-unused-vars
  try {
    LCMObject.setup();
  } catch (err) {
    console.log(err);
  }
}

function teardownLCM(event) { // eslint-disable-line no-unused-vars
  if (LCMObject.LCMInternal !== null) {
    LCMObject.LCMInternal.quit();
  }
}

app.on('ready', () => {
  Ansible.setup();
  ipcMain.on('LCM_CONFIG_CHANGE', LCMObject.changeLCMInfo);
  ipcMain.on('LCM_INITIALIZE', initializeLCM);
  ipcMain.on('LCM_TEARDOWN', teardownLCM);

  const mainWindow = new BrowserWindow();

  // Binding for the main process to inject into Redux workflow
  RendererBridge.registerWindow(mainWindow);

  mainWindow.maximize();
  mainWindow.loadURL(`file://${__dirname}/../static/index.html`);

  const menu = Menu.buildFromTemplate(Template);
  Menu.setApplicationMenu(menu);

  if (process.env.NODE_ENV !== 'production') {
    installExtension(REACT_DEVELOPER_TOOLS).then((name) => {
      console.log(`Added Extension:  ${name}`);
    }).catch((err) => {
      console.log('An error occurred: ', err);
    });

    installExtension(REDUX_DEVTOOLS).then((name) => {
      console.log(`Added Extension:  ${name}`);
    }).catch((err) => {
      console.log('An error occurred: ', err);
    });
  }
});
