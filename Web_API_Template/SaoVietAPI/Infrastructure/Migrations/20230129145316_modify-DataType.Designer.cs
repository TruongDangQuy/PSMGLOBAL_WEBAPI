﻿// <auto-generated />
using System;
using Infrastructure;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

#nullable disable

namespace Infrastructure.Migrations
{
    [DbContext(typeof(ApplicationDbContext))]
    [Migration("20230129145316_modify-DataType")]
    partial class modifyDataType
    {
        /// <inheritdoc />
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "7.0.2")
                .HasAnnotation("Relational:MaxIdentifierLength", 128);

            SqlServerModelBuilderExtensions.UseIdentityColumns(modelBuilder);

            modelBuilder.Entity("Domain.Entities.ApplicationUser", b =>
                {
                    b.Property<DateTime>("Id")
                        .HasColumnType("date");

                    b.Property<int>("AccessFailedCount")
                        .HasColumnType("int");

                    b.Property<DateTime?>("ConcurrencyStamp")
                        .IsConcurrencyToken()
                        .HasColumnType("date");

                    b.Property<DateTime?>("Email")
                        .HasMaxLength(256)
                        .HasColumnType("date");

                    b.Property<bool>("EmailConfirmed")
                        .HasColumnType("bit");

                    b.Property<bool>("LockoutEnabled")
                        .HasColumnType("bit");

                    b.Property<DateTimeOffset?>("LockoutEnd")
                        .HasColumnType("datetimeoffset");

                    b.Property<DateTime?>("NormalizedEmail")
                        .HasMaxLength(256)
                        .HasColumnType("date");

                    b.Property<DateTime?>("NormalizedUserName")
                        .HasMaxLength(256)
                        .HasColumnType("date");

                    b.Property<DateTime?>("PasswordHash")
                        .HasColumnType("date");

                    b.Property<DateTime?>("PhoneNumber")
                        .HasColumnType("date");

                    b.Property<bool>("PhoneNumberConfirmed")
                        .HasColumnType("bit");

                    b.Property<DateTime?>("SecurityStamp")
                        .HasColumnType("date");

                    b.Property<bool>("TwoFactorEnabled")
                        .HasColumnType("bit");

                    b.Property<DateTime?>("UserName")
                        .HasMaxLength(256)
                        .HasColumnType("date");

                    b.HasKey("Id");

                    b.HasIndex("NormalizedEmail")
                        .HasDatabaseName("EmailIndex");

                    b.HasIndex("NormalizedUserName")
                        .IsUnique()
                        .HasDatabaseName("UserNameIndex")
                        .HasFilter("[NormalizedUserName] IS NOT NULL");

                    b.ToTable("AspNetUsers", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Attendance", b =>
                {
                    b.Property<DateTime>("classId")
                        .HasColumnType("date");

                    b.Property<DateTime>("lessonId")
                        .HasColumnType("date");

                    b.Property<byte?>("attendance")
                        .HasColumnType("tinyint");

                    b.Property<DateTime?>("comment")
                        .HasColumnType("nvarchar(70)");

                    b.Property<DateTime>("date")
                        .HasColumnType("date");

                    b.Property<byte?>("evaluation")
                        .HasColumnType("tinyint");

                    b.HasKey("classId", "lessonId");

                    b.HasIndex("lessonId");

                    b.ToTable("Attendance", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Branch", b =>
                {
                    b.Property<DateTime>("id")
                        .HasColumnType("char(5)");

                    b.Property<DateTime?>("address")
                        .HasColumnType("nvarchar(80)");

                    b.Property<DateTime>("name")
                        .HasColumnType("nvarchar(50)");

                    b.HasKey("id");

                    b.ToTable("Branches", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Category", b =>
                {
                    b.Property<DateTime>("id")
                        .HasColumnType("char(5)");

                    b.Property<DateTime>("name")
                        .HasColumnType("nvarchar(25)");

                    b.HasKey("id");

                    b.ToTable("Categories", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Class", b =>
                {
                    b.Property<DateTime>("id")
                        .HasColumnType("char(7)");

                    b.Property<DateTime?>("branchId")
                        .HasColumnType("date");

                    b.Property<DateTime>("endDate")
                        .HasColumnType("date");

                    b.Property<DateTime>("name")
                        .HasColumnType("nvarchar(25)");

                    b.Property<DateTime>("startDate")
                        .HasColumnType("date");

                    b.Property<Guid?>("teacherId")
                        .HasColumnType("uniqueidentifier");

                    b.HasKey("id");

                    b.HasIndex("branchId");

                    b.HasIndex("teacherId");

                    b.ToTable("Classes", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.ClassStudent", b =>
                {
                    b.Property<DateTime>("classId")
                        .HasColumnType("date");

                    b.Property<Guid?>("studentId")
                        .HasColumnType("uniqueidentifier");

                    b.HasKey("classId", "studentId");

                    b.HasIndex("studentId");

                    b.ToTable("ClassStudents", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Course", b =>
                {
                    b.Property<DateTime>("id")
                        .HasColumnType("char(5)");

                    b.Property<DateTime?>("categoryId")
                        .HasColumnType("date");

                    b.Property<DateTime?>("description")
                        .HasColumnType("nvarchar(max)");

                    b.Property<DateTime>("name")
                        .HasColumnType("nvarchar(20)");

                    b.HasKey("id");

                    b.HasIndex("categoryId");

                    b.ToTable("Courses", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Lesson", b =>
                {
                    b.Property<DateTime>("id")
                        .HasColumnType("char(10)");

                    b.Property<DateTime?>("courseId")
                        .HasColumnType("date");

                    b.Property<DateTime?>("description")
                        .HasColumnType("nvarchar(max)");

                    b.Property<DateTime>("name")
                        .HasColumnType("nvarchar(50)");

                    b.HasKey("id");

                    b.HasIndex("courseId");

                    b.ToTable("Lessons", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Student", b =>
                {
                    b.Property<Guid?>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("uniqueidentifier");

                    b.Property<DateTime?>("dob")
                        .HasColumnType("date");

                    b.Property<DateTime>("email")
                        .HasColumnType("varchar(50)");

                    b.Property<DateTime>("fullName")
                        .HasColumnType("nvarchar(50)");

                    b.Property<DateTime?>("phone")
                        .HasColumnType("char(10)");

                    b.HasKey("id");

                    b.ToTable("Students", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Teacher", b =>
                {
                    b.Property<Guid>("id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("uniqueidentifier");

                    b.Property<DateTime?>("customerId")
                        .HasColumnType("date");

                    b.Property<DateTime>("email")
                        .HasColumnType("varchar(50)");

                    b.Property<DateTime>("fullName")
                        .HasColumnType("nvarchar(50)");

                    b.Property<DateTime?>("phone")
                        .HasColumnType("char(10)");

                    b.HasKey("id");

                    b.HasIndex("customerId");

                    b.ToTable("Teachers", (string)null);
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityRole", b =>
                {
                    b.Property<DateTime>("Id")
                        .HasColumnType("date");

                    b.Property<DateTime?>("ConcurrencyStamp")
                        .IsConcurrencyToken()
                        .HasColumnType("date");

                    b.Property<DateTime?>("Name")
                        .HasMaxLength(256)
                        .HasColumnType("date");

                    b.Property<DateTime?>("NormalizedName")
                        .HasMaxLength(256)
                        .HasColumnType("date");

                    b.HasKey("Id");

                    b.HasIndex("NormalizedName")
                        .IsUnique()
                        .HasDatabaseName("RoleNameIndex")
                        .HasFilter("[NormalizedName] IS NOT NULL");

                    b.ToTable("AspNetRoles", (string)null);
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityRoleClaim<string>", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<DateTime?>("ClaimType")
                        .HasColumnType("date");

                    b.Property<DateTime?>("ClaimValue")
                        .HasColumnType("date");

                    b.Property<DateTime>("RoleId")
                        .HasColumnType("date");

                    b.HasKey("Id");

                    b.HasIndex("RoleId");

                    b.ToTable("AspNetRoleClaims", (string)null);
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserClaim<string>", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"));

                    b.Property<DateTime?>("ClaimType")
                        .HasColumnType("date");

                    b.Property<DateTime?>("ClaimValue")
                        .HasColumnType("date");

                    b.Property<DateTime>("UserId")
                        .HasColumnType("date");

                    b.HasKey("Id");

                    b.HasIndex("UserId");

                    b.ToTable("AspNetUserClaims", (string)null);
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>
                {
                    b.Property<DateTime>("LoginProvider")
                        .HasColumnType("date");

                    b.Property<DateTime>("ProviderKey")
                        .HasColumnType("date");

                    b.Property<DateTime?>("ProviderDisplayName")
                        .HasColumnType("date");

                    b.Property<DateTime>("UserId")
                        .HasColumnType("date");

                    b.HasKey("LoginProvider", "ProviderKey");

                    b.HasIndex("UserId");

                    b.ToTable("AspNetUserLogins", (string)null);
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserRole<string>", b =>
                {
                    b.Property<DateTime>("UserId")
                        .HasColumnType("date");

                    b.Property<DateTime>("RoleId")
                        .HasColumnType("date");

                    b.HasKey("UserId", "RoleId");

                    b.HasIndex("RoleId");

                    b.ToTable("AspNetUserRoles", (string)null);
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserToken<string>", b =>
                {
                    b.Property<DateTime>("UserId")
                        .HasColumnType("date");

                    b.Property<DateTime>("LoginProvider")
                        .HasColumnType("date");

                    b.Property<DateTime>("Name")
                        .HasColumnType("date");

                    b.Property<DateTime?>("Value")
                        .HasColumnType("date");

                    b.HasKey("UserId", "LoginProvider", "Name");

                    b.ToTable("AspNetUserTokens", (string)null);
                });

            modelBuilder.Entity("Domain.Entities.Attendance", b =>
                {
                    b.HasOne("Domain.Entities.Class", "class")
                        .WithMany("attendances")
                        .HasForeignKey("classId")
                        .OnDelete(DeleteBehavior.NoAction)
                        .IsRequired();

                    b.HasOne("Domain.Entities.Lesson", "lesson")
                        .WithMany("attendances")
                        .HasForeignKey("lessonId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("class");

                    b.Navigation("lesson");
                });

            modelBuilder.Entity("Domain.Entities.Class", b =>
                {
                    b.HasOne("Domain.Entities.Branch", "branch")
                        .WithMany("classes")
                        .HasForeignKey("branchId")
                        .OnDelete(DeleteBehavior.SetNull);

                    b.HasOne("Domain.Entities.Teacher", "teacher")
                        .WithMany("classes")
                        .HasForeignKey("teacherId")
                        .OnDelete(DeleteBehavior.SetNull);

                    b.Navigation("branch");

                    b.Navigation("teacher");
                });

            modelBuilder.Entity("Domain.Entities.ClassStudent", b =>
                {
                    b.HasOne("Domain.Entities.Class", "class")
                        .WithMany("classStudents")
                        .HasForeignKey("classId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("Domain.Entities.Student", "student")
                        .WithMany("classStudents")
                        .HasForeignKey("studentId")
                        .OnDelete(DeleteBehavior.NoAction)
                        .IsRequired();

                    b.Navigation("class");

                    b.Navigation("student");
                });

            modelBuilder.Entity("Domain.Entities.Course", b =>
                {
                    b.HasOne("Domain.Entities.Category", "category")
                        .WithMany("courses")
                        .HasForeignKey("categoryId")
                        .OnDelete(DeleteBehavior.SetNull);

                    b.Navigation("category");
                });

            modelBuilder.Entity("Domain.Entities.Lesson", b =>
                {
                    b.HasOne("Domain.Entities.Course", "course")
                        .WithMany("lessons")
                        .HasForeignKey("courseId")
                        .OnDelete(DeleteBehavior.SetNull);

                    b.Navigation("course");
                });

            modelBuilder.Entity("Domain.Entities.Teacher", b =>
                {
                    b.HasOne("Domain.Entities.ApplicationUser", "customer")
                        .WithMany("teachers")
                        .HasForeignKey("customerId")
                        .OnDelete(DeleteBehavior.SetNull);

                    b.Navigation("customer");
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityRoleClaim<string>", b =>
                {
                    b.HasOne("Microsoft.AspNetCore.Identity.IdentityRole", null)
                        .WithMany()
                        .HasForeignKey("RoleId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserClaim<string>", b =>
                {
                    b.HasOne("Domain.Entities.ApplicationUser", null)
                        .WithMany()
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserLogin<string>", b =>
                {
                    b.HasOne("Domain.Entities.ApplicationUser", null)
                        .WithMany()
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserRole<string>", b =>
                {
                    b.HasOne("Microsoft.AspNetCore.Identity.IdentityRole", null)
                        .WithMany()
                        .HasForeignKey("RoleId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("Domain.Entities.ApplicationUser", null)
                        .WithMany()
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();
                });

            modelBuilder.Entity("Microsoft.AspNetCore.Identity.IdentityUserToken<string>", b =>
                {
                    b.HasOne("Domain.Entities.ApplicationUser", null)
                        .WithMany()
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();
                });

            modelBuilder.Entity("Domain.Entities.ApplicationUser", b =>
                {
                    b.Navigation("teachers");
                });

            modelBuilder.Entity("Domain.Entities.Branch", b =>
                {
                    b.Navigation("classes");
                });

            modelBuilder.Entity("Domain.Entities.Category", b =>
                {
                    b.Navigation("courses");
                });

            modelBuilder.Entity("Domain.Entities.Class", b =>
                {
                    b.Navigation("attendances");

                    b.Navigation("classStudents");
                });

            modelBuilder.Entity("Domain.Entities.Course", b =>
                {
                    b.Navigation("lessons");
                });

            modelBuilder.Entity("Domain.Entities.Lesson", b =>
                {
                    b.Navigation("attendances");
                });

            modelBuilder.Entity("Domain.Entities.Student", b =>
                {
                    b.Navigation("classStudents");
                });

            modelBuilder.Entity("Domain.Entities.Teacher", b =>
                {
                    b.Navigation("classes");
                });
#pragma warning restore 612, 618
        }
    }
}