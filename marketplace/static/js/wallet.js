// Wallet Connection Manager for SormatSea.io NFT Marketplace
class WalletManager {
    constructor() {
        this.web3 = null;
        this.account = null;
        this.chainId = null;
        this.isConnected = false;
        this.supportedChainIds = {
            1: 'Ethereum Mainnet',
            3: 'Ropsten Testnet',
            4: 'Rinkeby Testnet',
            5: 'Goerli Testnet',
            56: 'BSC Mainnet',
            97: 'BSC Testnet',
            137: 'Polygon Mainnet',
            80001: 'Mumbai Testnet'
        };
    }

    async init() {
        // Check if wallet was previously connected
        await this.checkConnection();
        
        // Setup event listeners for wallet buttons
        this.setupWalletButtonListeners();
        
        // Listen for account changes
        this.setupWalletEventListeners();
        
        // Update UI
        this.updateWalletUI();
    }

    setupWalletButtonListeners() {
        // Event listener approach for wallet buttons
        const walletButtons = document.querySelectorAll('.wallet-btn');
        
        walletButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const walletType = button.getAttribute('data-wallet');
                this.connectSpecificWallet(walletType);
            });
        });

        // Also setup the main wallet connect button
        const mainWalletButton = document.getElementById('walletButton');
        if (mainWalletButton) {
            mainWalletButton.addEventListener('click', (e) => {
                e.preventDefault();
                if (this.isConnected) {
                    this.showWalletInfo();
                } else {
                    this.showWalletOptions();
                }
            });
        }
    }

    async connectSpecificWallet(walletType) {
        console.log(`Connecting to ${walletType}...`);
        
        // Show loading state
        this.updateWalletButton(`Connecting to ${walletType}...`, true);

        try {
            switch(walletType) {
                case 'tonkeeper':
                    await this.connectTonkeeper();
                    break;
                case 'metamask':
                    await this.connectMetaMask();
                    break;
                case 'trustwallet':
                    await this.connectTrustWallet();
                    break;
                case 'walletconnect':
                    await this.connectWalletConnect();
                    break;
                case 'coinbase':
                    await this.connectCoinbase();
                    break;
                default:
                    throw new Error('Unsupported wallet type');
            }
        } catch (error) {
            this.handleWalletError(error);
        }
    }

    async connectTonkeeper() {
        // Tonkeeper-specific connection logic
        if (typeof window.ton !== 'undefined') {
            try {
                const accounts = await window.ton.send('ton_requestAccounts');
                this.handleSuccessfulConnection(accounts[0], 'tonkeeper');
            } catch (error) {
                throw new Error('Tonkeeper connection failed');
            }
        } else {
            // Fallback: open Tonkeeper download page
            window.open('https://tonkeeper.com/', '_blank');
            throw new Error('Tonkeeper not detected. Please install the extension.');
        }
    }

    async connectMetaMask() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                const accounts = await window.ethereum.request({
                    method: 'eth_requestAccounts'
                });
                this.handleSuccessfulConnection(accounts[0], 'metamask');
            } catch (error) {
                throw new Error('MetaMask connection failed');
            }
        } else {
            window.open('https://metamask.io/download.html', '_blank');
            throw new Error('MetaMask not detected. Please install the extension.');
        }
    }

    async connectTrustWallet() {
        if (typeof window.ethereum !== 'undefined' && window.ethereum.isTrust) {
            try {
                const accounts = await window.ethereum.request({
                    method: 'eth_requestAccounts'
                });
                this.handleSuccessfulConnection(accounts[0], 'trustwallet');
            } catch (error) {
                throw new Error('Trust Wallet connection failed');
            }
        } else {
            window.open('https://trustwallet.com/download', '_blank');
            throw new Error('Trust Wallet not detected.');
        }
    }

    async connectWalletConnect() {
        // WalletConnect implementation would go here
        this.showSuccessMessage('WalletConnect selected - implementation required');
    }

    async connectCoinbase() {
        if (typeof window.ethereum !== 'undefined' && window.ethereum.isCoinbaseWallet) {
            try {
                const accounts = await window.ethereum.request({
                    method: 'eth_requestAccounts'
                });
                this.handleSuccessfulConnection(accounts[0], 'coinbase');
            } catch (error) {
                throw new Error('Coinbase Wallet connection failed');
            }
        } else {
            window.open('https://www.coinbase.com/wallet', '_blank');
            throw new Error('Coinbase Wallet not detected.');
        }
    }

    handleSuccessfulConnection(address, walletType) {
        this.account = address;
        this.isConnected = true;
        this.walletType = walletType;

        // Save connection state
        localStorage.setItem('walletConnected', 'true');
        localStorage.setItem('walletAddress', this.account);
        localStorage.setItem('walletType', walletType);

        this.updateWalletUI();
        this.showSuccessMessage(`Connected to ${walletType} successfully!`);

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('walletConnected', {
            detail: { 
                address: this.account, 
                walletType: walletType,
                chainId: this.chainId 
            }
        }));
    }

    // ... rest of your existing methods (checkConnection, setupEventListeners, etc.) ...

    showWalletOptions() {
        // Create modal for wallet options
        const modal = document.createElement('div');
        modal.className = 'wallet-modal';
        modal.innerHTML = `
            <div class="wallet-modal-content">
                <div class="wallet-modal-header">
                    <h5>Connect Your Wallet</h5>
                    <button class="btn-close">&times;</button>
                </div>
                <div class="wallet-modal-body">
                    <div class="wallet-options">
                        <button class="wallet-btn" data-wallet="metamask">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg" 
                                 alt="MetaMask" class="wallet-icon">
                            <div>
                                <strong>MetaMask</strong>
                                <p>Browser extension wallet</p>
                            </div>
                        </button>
                        <button class="wallet-btn" data-wallet="trustwallet">
                            <img src="https://trustwallet.com/assets/images/media/assets/horizontal_blue.png" 
                                 alt="Trust Wallet" class="wallet-icon">
                            <div>
                                <strong>Trust Wallet</strong>
                                <p>Mobile wallet</p>
                            </div>
                        </button>
                        <button class="wallet-btn" data-wallet="tonkeeper">
                            <img src="https://tonkeeper.com/assets/tonconnect-icon.png" 
                                 alt="Tonkeeper" class="wallet-icon">
                            <div>
                                <strong>Tonkeeper</strong>
                                <p>TON blockchain wallet</p>
                            </div>
                        </button>
                        <button class="wallet-btn" data-wallet="coinbase">
                            <img src="https://avatars.githubusercontent.com/u/18060234?s=280&v=4" 
                                 alt="Coinbase" class="wallet-icon">
                            <div>
                                <strong>Coinbase Wallet</strong>
                                <p>Exchange wallet</p>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        
        // Setup event listeners for modal buttons
        const closeBtn = modal.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => modal.remove());

        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        // Setup wallet button listeners within the modal
        const walletButtons = modal.querySelectorAll('.wallet-btn');
        walletButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const walletType = button.getAttribute('data-wallet');
                modal.remove();
                this.connectSpecificWallet(walletType);
            });
        });
    }
}

// Initialize wallet manager
let walletManager;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    walletManager = new WalletManager();
    walletManager.init();
});

function connectWallet(walletType = null) {
    if (!walletManager) return;
    
    if (walletType) {
        walletManager.connectSpecificWallet(walletType);
    } else if (walletManager.isConnected) {
        walletManager.showWalletInfo();
    } else {
        walletManager.showWalletOptions();
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WalletManager;
}