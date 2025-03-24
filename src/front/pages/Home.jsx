import React from "react";

const Home = () => {
	return (
		<div className="container-fluid bg-light">
			{/* Navbar */}
			<nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
				<div className="container">
					<a className="navbar-brand text-pink" href="#">Uñas Perfectas</a>
					<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
						<span className="navbar-toggler-icon"></span>
					</button>
					<div className="collapse navbar-collapse" id="navbarNav">
						<ul className="navbar-nav ms-auto">
							<li className="nav-item"><a className="nav-link" href="#">Inicio</a></li>
							<li className="nav-item"><a className="nav-link" href="#">Diseños</a></li>
							<li className="nav-item"><a className="nav-link" href="#">Contacto</a></li>
						</ul>
					</div>
				</div>
			</nav>

			{/* Hero Section */}
			<header className="text-center py-5 bg-pink text-white">
				<h1>Bienvenida a Uñas Perfectas</h1>
				<p>Descubre los diseños más increíbles para tus uñas</p>
			</header>

			{/* Galería de Diseños */}
			<section className="container my-5">
				<h2 className="text-center text-pink">Últimos Diseños</h2>
				<div className="row">
					{[1, 2, 3, 4, 5, 6].map((item) => (
						<div key={item} className="col-md-4 mb-4">
							<div className="card shadow-sm">
								<img
									src={`https://source.unsplash.com/300x200/?nails,design&random=${item}`}
									className="card-img-top"
									alt="Diseño de uñas"
								/>
								<div className="card-body">
									<h5 className="card-title text-pink">Diseño {item}</h5>
									<p className="card-text">Un diseño único y espectacular para tus uñas.</p>
								</div>
							</div>
						</div>
					))}
				</div>
			</section>

			{/* Footer */}
			<footer className="text-center py-4 bg-white shadow-sm">
				<p className="mb-0">&copy; 2025 Uñas Perfectas - Todos los derechos reservados</p>
			</footer>
		</div>
	);
};

export default Home;
