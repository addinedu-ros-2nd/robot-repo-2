#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/segmentation/impl/extract_clusters.hpp>

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " input.pcd output.pcd" << std::endl;
        return -1;
    }

    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    if (pcl::io::loadPCDFile<pcl::PointXYZ>(argv[1], *cloud) == -1) {
        PCL_ERROR("Couldn't read file\n");
        return -1;
    }

    pcl::search::KdTree<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>);
    tree->setInputCloud(cloud);

    std::vector<pcl::PointIndices> cluster_indices;
    pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
    ec.setClusterTolerance(0.02); // 클러스터 간의 거리 허용 범위
    ec.setMinClusterSize(100);   // 클러스터 최소 크기
    ec.setMaxClusterSize(25000);  // 클러스터 최대 크기
    ec.setSearchMethod(tree);
    ec.setInputCloud(cloud);
    ec.extract(cluster_indices);

    pcl::PointCloud<pcl::PointXYZRGB>::Ptr colored_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);

    for (size_t i = 0; i < cluster_indices.size(); ++i) {
        uint8_t r = static_cast<uint8_t>((i * 50) % 255);
        uint8_t g = static_cast<uint8_t>((255 - i * 50) % 255);

        for (const auto& index : cluster_indices[i].indices) {
            pcl::PointXYZRGB p;
            p.x = cloud->points[index].x;
            p.y = cloud->points[index].y;
            p.z = cloud->points[index].z;

            p.r = r;
            p.g = g;
            p.b = 0;

            colored_cloud->points.push_back(p);
        }
    }

    colored_cloud->width = colored_cloud->points.size();
    colored_cloud->height = 1;
    colored_cloud->is_dense = true;

    pcl::io::savePCDFileASCII(argv[2], *colored_cloud);

    return 0;
}
