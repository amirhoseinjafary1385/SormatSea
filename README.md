# 🚀 SormatSea - NFT Marketplace

[![Django Version](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A modern, feature-rich NFT marketplace built with Django, allowing users to discover, collect, and trade unique digital assets across multiple blockchains.

## 📸 Screenshots

<!-- Add screenshots here -->
<!-- ![Homepage](screenshots/home.png) -->
<!-- ![NFT Detail](screenshots/nft-detail.png) -->
<!-- ![Wallet Connect](screenshots/wallet-connect.png) -->

## ✨ Features

### 🎨 Core Features
- **NFT Management**: Create, list, and manage NFTs with detailed metadata
- **Multi-Blockchain Support**: TON, Ethereum, Polygon, Binance Smart Chain, Solana, Avalanche
- **Advanced Search**: Search NFTs by name, category, tags, and price range
- **Categories & Subcategories**: Organized browsing with nested categories
- **User Authentication**: Register, login, password reset with email verification
- **Wallet Integration**: Connect multiple wallet providers (MetaMask, Tonkeeper, Trust Wallet)
- **Shopping Cart**: Add NFTs to cart, update quantities, and checkout
- **Secure Payments**: Multiple payment methods including crypto and fiat

### 🛒 User Features
- **User Profiles**: Custom avatars, bio, social links, wallet addresses
- **Favorites & Likes**: Save favorite NFTs and like items
- **Reviews & Ratings**: Rate NFTs and leave reviews (verified purchases only)
- **Notifications**: Real-time notifications for purchases, bids, and system updates
- **Activity Logging**: Track views, likes, favorites, and shares

### 📊 Admin Features
- **Dashboard**: Overview of marketplace statistics
- **User Management**: Manage users, verify profiles, handle disputes
- **NFT Moderation**: Approve/reject listings, verify authenticity
- **Transaction Monitoring**: Track all transactions with status
- **Content Management**: Manage categories, subcategories, and featured NFTs

### 💰 E-commerce Features
- **Dynamic Pricing**: Support for multiple currencies (IRT, ETH, BNB, SOL)
- **Discount System**: Percentage-based discounts with date ranges
- **Royalty System**: Creator royalties (up to 50%)
- **Platform Fees**: Automatic fee calculation (2.5%)
- **Transaction History**: Complete purchase history with status tracking
- **Auction Support**: Place bids on auction-style NFTs

### 🎯 Technical Features
- **Responsive Design**: Mobile-first, works on all devices
- **Dark/Light Theme**: User preference saved in localStorage
- **Web3 Integration**: Connect to blockchain wallets
- **REST API Ready**: Extensible for mobile apps
- **SEO Friendly**: Meta tags, slugs, and clean URLs
- **Performance Optimized**: Database indexing, caching ready

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Django's built-in auth system
- **Payments**: Stripe, PayPal, Crypto (custom implementation)
- **Email**: Django's email backend (console for development)

### Frontend
- **CSS Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6, Bootstrap Icons
- **Carousel**: Glide.js
- **JavaScript**: Vanilla JS with Web3.js
- **Templates**: Django Template Language

### Blockchain
- **TON**: Tonkeeper integration
- **Ethereum**: MetaMask integration
- **Multi-Chain**: Support for Polygon, BSC, Solana, Avalanche

## 📁 Project Structure
