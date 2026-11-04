<?php

namespace App\Controller;

use App\Entity\Product;
use App\Form\ProductoType;
use App\Repository\ProductRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/productos', name: 'app_producto_')]
final class ProductController extends AbstractController
{
    #[Route('', name: 'index', methods: ['GET'])]
    public function index(ProductRepository $repo): Response
    {
        $productos = $repo->findBy(['activo' => true]);

        return $this->render('product/index.html.twig', [
            'productos' => $productos,
        ]);
    }

    #[Route('/crear', name: 'crear', methods: ['GET', 'POST'])]
    public function crear(Request $request, EntityManagerInterface $em): Response
    {
        $producto = new Product();
        $producto->setFechaCreacion(new \DateTime());
        $producto->setActivo(true);

        $form = $this->createForm(ProductoType::class, $producto);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $em->persist($producto);
            $em->flush();

            return $this->redirectToRoute('app_producto_index');
        }

        return $this->render('product/crear.html.twig', [
            'form' => $form->createView(),
        ]);
    }

    #[Route('/{id}', name: 'detalle', methods: ['GET'])]
    public function detalle(int $id, ProductRepository $repo): Response
    {
        $producto = $repo->find($id);

        if (!$producto) {
            throw $this->createNotFoundException('El producto solicitado no existe');
        }

        return $this->render('product/detalle.html.twig', [
            'producto' => $producto,
        ]);
    }
}
